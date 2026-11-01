import io
import json
import os
import struct
import zipfile

import pytest

import iff_ls

NEAR_JSON = '''"hihead": {
\t"EndTime": 2.0,
\t"Material": {
\t\t"torso_shader": ,
\t\t"face_shader": 
\t},
\t"Model": {
\t\t"player": {
\t\t\t"Node": {
\t\t\t\t"def_hips": { "Child": 1 },
\t\t\t\t"def_spine": { "Child": 2, "Sibling": 3, "Pos": [ 0.0, 8.15, 0.0 ] },
\t\t\t\t"def_spine1": { "Pos": [ 0.0, 12.22, 0.0 ] },
\t\t\t\t"def_l_leg": { "Pos": [ 1.0, 0.0, 0.0 ] }
\t\t\t}
\t\t}
\t},
\t"Mathnode": {
\t\t{ "MathnodeBinary": "a.mathnodes" }
\t}
}'''


def make_iff(tmp_path):
    path = tmp_path / "sample.iff"
    rdat_payload = b'{ "RIGTYPE": "MALE", "SKINCOLOR": 4 }'
    rdat = struct.pack("<IIII", len(rdat_payload), 0, 9, 0) + rdat_payload
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hihead.SCNE", NEAR_JSON)
        z.writestr("player.abc.model", bytes.fromhex("453c46b2") + b"\0" * 32)
        z.writestr("appearance_info.RDAT", rdat)
        z.writestr("tex.bin", b"DDS " + b"\0" * 20)
    return str(path)


def test_list_entries_classifies_by_magic_and_extension(tmp_path):
    entries = iff_ls.list_entries(make_iff(tmp_path))
    kinds = {e.name: e.kind for e in entries}
    assert kinds == {
        "hihead.SCNE": "scene-json",
        "player.abc.model": "model-mesh",
        "appearance_info.RDAT": "record-json",
        "tex.bin": "dds-texture",
    }


def test_repair_json_handles_empty_values_and_anonymous_objects():
    obj = json.loads(iff_ls.repair_json(NEAR_JSON))
    assert obj["hihead"]["Material"] == {"torso_shader": None, "face_shader": None}
    assert obj["hihead"]["Mathnode"]["_1"]["MathnodeBinary"] == "a.mathnodes"


def test_rdat_prefix_is_stripped(tmp_path):
    rec = iff_ls.read_json_entry(make_iff(tmp_path), "appearance_info.RDAT")
    assert rec == {"RIGTYPE": "MALE", "SKINCOLOR": 4}


def test_skeleton_resolves_child_and_sibling_links(tmp_path):
    scene = iff_ls.read_json_entry(make_iff(tmp_path), "hihead.SCNE")
    rows = iff_ls.skeleton(scene)
    assert rows == [
        ("def_hips", None, None),
        ("def_spine", "def_hips", [0.0, 8.15, 0.0]),
        ("def_spine1", "def_spine", [0.0, 12.22, 0.0]),
        ("def_l_leg", "def_hips", [1.0, 0.0, 0.0]),  # sibling of def_spine shares its parent
    ]


@pytest.mark.skipif(not os.environ.get("IFF_SAMPLE"), reason="set IFF_SAMPLE=/path/to/real.iff")
def test_real_file_smoke():
    path = os.environ["IFF_SAMPLE"]
    entries = iff_ls.list_entries(path)
    assert any(e.kind == "scene-json" for e in entries)
    scne = next(e.name for e in entries if e.kind == "scene-json")
    rows = iff_ls.skeleton(iff_ls.read_json_entry(path, scne))
    assert rows[0][0] == "def_hips" and len(rows) > 50
