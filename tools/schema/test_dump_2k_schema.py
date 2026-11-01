import json

import dump_2k_schema


def test_render_emits_names_without_addresses(tmp_path):
    (tmp_path / "offsets_players.json").write_text(json.dumps({
        "Players": {"Attributes": {"Offense": [
            {"normalized_name": "3POINT", "display_name": "3pt Shot",
             "versions": {"2K26": {"address": 1001, "length": 8}}},
            {"normalized_name": "HANDS", "versions": {}},
        ]}}
    }))
    md = dump_2k_schema.render(tmp_path)
    assert "### Attributes / Offense (2) versions: 2K26" in md
    assert "3pt Shot, HANDS" in md
    assert "1001" not in md
