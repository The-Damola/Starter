"""List and inspect NBA 2K .iff containers (2K16-2K20 era: a ZIP with game-specific entries).

Usage:
    python tools/iff/iff_ls.py FILE.iff            # list entries with detected kind
    python tools/iff/iff_ls.py FILE.iff --skeleton # print joint tree from the SCNE scene entry
    python tools/iff/iff_ls.py FILE.iff --json ENTRY  # dump a SCNE/RDAT entry as repaired JSON

Facts this encodes (verified on a 2K17 face file, see docs/research/iff-format.md):
- The container is a standard ZIP (deflate). Python's zipfile opens it.
- .SCNE and .RDAT entries are near-JSON: empty values (`"k": ,`), anonymous
  nested objects (`{ { ... } }`), and RDAT has a 16-byte binary prefix.
- The SCNE "Node" map is the skeleton: Child/Sibling are indices into node
  order; Pos is the local offset from the parent.
"""
from __future__ import annotations

import argparse
import json
import re
import signal
import struct
import sys
import zipfile
from dataclasses import dataclass

MAGIC_KINDS = {
    b"DDS ": "dds-texture",
    b"\x89PNG": "png",
    b"E<F\xb2": "model-mesh",  # 0x453C46B2, seen on 2K17 .model entries
}


@dataclass
class Entry:
    name: str
    size: int
    compressed: int
    kind: str


def classify(name: str, head: bytes) -> str:
    for magic, kind in MAGIC_KINDS.items():
        if head.startswith(magic):
            return kind
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return {
        "scne": "scene-json",
        "rdat": "record-json",
        "mathnodes": "mathnodes-binary",
        "model": "model-mesh",
    }.get(ext, "unknown")


GEN1_MAGICS = {
    bytes.fromhex("305098f0"): "gen-1 IFF, little-endian (NBA 2K9-2K14 PC)",
    bytes.fromhex("ff3bef94"): "gen-1 IFF, big-endian (College Hoops 2K8 / 2K8-era consoles)",
}


def gen1_header(path: str) -> dict | None:
    """Describe a pre-2K15 container. Sub-file parsing is not implemented; see docs/research/iff-format.md."""
    with open(path, "rb") as f:
        head = f.read(0x20)
    kind = GEN1_MAGICS.get(head[:4])
    if kind is None:
        return None
    endian = "<" if "little" in kind else ">"
    header_size, _file_len_be, _zero, block_count, _u1, file_count, _u2 = struct.unpack(endian + "7I", head[4:32])
    return {"kind": kind, "header_size": header_size, "block_count": block_count, "file_count": file_count}


def list_entries(path: str) -> list[Entry]:
    if not zipfile.is_zipfile(path):
        info = gen1_header(path)
        if info:
            raise NotImplementedError(
                f"{info['kind']}: header {info['header_size']} bytes, {info['block_count']} block(s), "
                f"{info['file_count']} sub-files. Only the ZIP-era (2K15+) layout is parsed."
            )
        raise ValueError("not a ZIP-era .iff and no known gen-1 magic")
    with zipfile.ZipFile(path) as z:
        out = []
        for info in z.infolist():
            with z.open(info) as f:
                head = f.read(16)
            out.append(Entry(info.filename, info.file_size, info.compress_size, classify(info.filename, head)))
        return out


def repair_json(text: str) -> str:
    """Turn 2K's near-JSON into strict JSON."""
    text = re.sub(r":\s*(?=[,}\r\n])", ": null", text)  # empty values
    counter = [0]

    def name_anonymous(m: re.Match) -> str:
        counter[0] += 1
        return f'{m.group(1)}{m.group(2)}"_{counter[0]}": {{'

    text = re.sub(r"([{,])(\s*)\{", name_anonymous, text)  # anonymous objects
    text = re.sub(r",(\s*[}\]])", r"\1", text)  # trailing commas
    text = text.strip()
    if not text.startswith("{"):
        text = "{" + text + "}"
    return text


def read_json_entry(path: str, entry: str) -> dict:
    with zipfile.ZipFile(path) as z:
        raw = z.read(entry)
    if entry.lower().endswith(".rdat"):
        # 16-byte prefix: two little-endian uint32 (payload length, record count?) then padding.
        payload_len = struct.unpack_from("<I", raw, 0)[0]
        raw = raw[16 : 16 + payload_len]
    return json.loads(repair_json(raw.decode("latin1")))


def skeleton(scene: dict) -> list[tuple[str, str | None, list[float] | None]]:
    """Return (joint, parent, local_pos) rows in file order from a SCNE dict."""
    root = next(iter(scene.values()))
    model = next(iter(root["Model"].values()))
    nodes = model["Node"]
    names = list(nodes)
    parent: dict[int, int | None] = {0: None}
    for i, name in enumerate(names):
        node = nodes[name]
        if "Child" in node:
            parent[node["Child"]] = i
        if "Sibling" in node:
            parent[node["Sibling"]] = parent.get(i)
    rows = []
    for i, name in enumerate(names):
        p = parent.get(i)
        rows.append((name, names[p] if p is not None else None, nodes[name].get("Pos")))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("iff")
    ap.add_argument("--skeleton", action="store_true", help="print joint tree from the first SCNE entry")
    ap.add_argument("--json", metavar="ENTRY", help="dump a SCNE/RDAT entry as strict JSON")
    args = ap.parse_args(argv)

    if args.json:
        json.dump(read_json_entry(args.iff, args.json), sys.stdout, indent=1)
        print()
        return 0

    try:
        entries = list_entries(args.iff)
    except (NotImplementedError, ValueError) as e:
        print(e, file=sys.stderr)
        return 2
    if args.skeleton:
        scne = next((e.name for e in entries if e.kind == "scene-json"), None)
        if scne is None:
            print("no SCNE entry found", file=sys.stderr)
            return 1
        for joint, parent, pos in skeleton(read_json_entry(args.iff, scne)):
            print(f"{joint:36s} parent={parent or '-':30s} pos={pos}")
        return 0

    for e in entries:
        print(f"{e.name:44s} {e.kind:18s} {e.size:>10,d} bytes  ({e.compressed:,d} compressed)")
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped into head
    raise SystemExit(main())
