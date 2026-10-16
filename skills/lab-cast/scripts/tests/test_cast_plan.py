import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cast_plan  # noqa: E402

CATALOGUE = Path(__file__).resolve().parent.parent.parent / "catalogue"


def plan_for(tmp_path, body):
    path = tmp_path / "profile.toml"
    path.write_text(body, encoding="utf-8")
    profile = tomllib.loads(body)
    rules, methods, packs = cast_plan.load_catalogue(CATALOGUE)
    return cast_plan.plan(profile, rules, methods, packs), path


def test_quantum_project_uses_packs_and_formal_methods(tmp_path):
    result, _ = plan_for(tmp_path, '''
[project]
slug = "shift-winding"
title = "Shift winding of quantum states"
[classification]
fields = ["1.3 Physical sciences", "1.1 Mathematics"]
subfields = ["quantum information", "complex analysis"]
modes = ["formal", "computational"]
outputs = ["paper", "software"]
''')
    assert result["ok"], result["errors"]
    assert {p["id"] for p in result["packs"]} == {"quantum", "physics", "mathematics"}
    assert {p["name"] for p in result["pack_personas"]} >= {"Sofia Marchetti", "Ignacio Valdivieso", "Kwame Mensah", "Ruolan Qiao"}
    assert {p["code"] for p in result["methods"]} == {"lab-method-formalist", "lab-method-calculator", "lab-method-simulation"}
    assert result["stories"][:2] == ["THM", "LEM"] and "CODE" in result["stories"] and "FORMAL" in result["stories"]
    assert [g["for"] for g in result["generate"]] == ["complex analysis", "the people who would use the result"]
    assert "zbMATH Open" in result["search"] and "INSPIRE-HEP" in result["search"]
    rooms = {r["id"]: r for r in result["rooms"]}
    assert set(rooms) == {"shift-winding-seminar", "shift-winding-tribunal", "shift-winding-proof"}
    assert "pack-quantum-dequantizer" in rooms["shift-winding-tribunal"]["members"]
    assert result["guardians"] == []


def test_social_science_study_brings_guardians_and_generates_experts(tmp_path):
    result, _ = plan_for(tmp_path, '''
[project]
slug = "credit-survey"
title = "How households read credit scores"
[classification]
fields = ["5.2 Economics and business", "5.1 Psychology"]
subfields = ["household finance", "behavioural economics"]
modes = ["observational", "qualitative"]
outputs = ["paper", "dataset"]
sensitivities = ["human-participants", "personal-data"]
''')
    assert result["ok"], result["errors"]
    assert result["packs"] == [] and len(result["generate"]) == 2
    assert set(result["guardians"]) == {"lab-guest-ethics", "lab-guest-dataprotection"}
    assert {"STUDY", "DATA", "WRITE", "LIT", "DECIDE"} <= set(result["stories"]) and "THM" not in result["stories"]
    assert any("IRB" in g for g in result["gates"]) and any("no personal data" in g for g in result["gates"])
    assert "RePEc/IDEAS" in result["search"] and "PsycINFO" in result["search"]
    assert {p["code"] for p in result["methods"]} == {"lab-method-causal", "lab-method-qualitative"}
    rooms = {r["id"]: r for r in result["rooms"]}
    assert "credit-survey-proof" not in rooms
    assert "lab-guest-ethics" in rooms["credit-survey-tribunal"]["members"]
    assert rooms["credit-survey-seminar"]["add_generated"] == ["core-a", "core-b", "translator"]


def test_errors_for_unknown_codes(tmp_path):
    result, _ = plan_for(tmp_path, '''
[classification]
fields = ["9.9"]
modes = ["vibes"]
sensitivities = ["secret"]
''')
    assert not result["ok"]
    joined = " ".join(result["errors"])
    assert "unknown field code" in joined and "unknown mode" in joined and "unknown sensitivity" in joined


def test_cli_and_party_toml(tmp_path, capsys):
    _, path = plan_for(tmp_path, '''
[project]
slug = "mt"
title = "Model theory of quantum mechanics"
[classification]
fields = ["1.1"]
subfields = ["model theory"]
modes = ["formal"]
outputs = ["paper"]
''')
    assert cast_plan.main([str(path), "--format", "toml"]) == 0
    toml_text = capsys.readouterr().out
    data = tomllib.loads(toml_text)
    codes = {m["code"] for m in data["workflow"]["party_members"]}
    assert {"pack-math-mathematician", "lab-method-formalist"} <= codes
    assert ".agents/skills/lab-cast/playbooks/formalize.md" in toml_text
    assert {g["id"] for g in data["workflow"]["party_groups"]} == {"mt-seminar", "mt-tribunal", "mt-proof"}
    assert cast_plan.main([str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["generate"][0]["for"] == "model theory"
    assert cast_plan.main([str(tmp_path / "missing.toml")]) == 2


def test_catalogue_is_well_formed():
    """Guards contributed packs and specialists: known codes, unique names, real playbooks."""
    rules, methods, packs = cast_plan.load_catalogue(CATALOGUE)
    playbooks = {p.stem for p in (CATALOGUE.parent / "playbooks").glob("*.md")}
    codes = [m["code"] for m in methods]
    for m in methods:
        assert m["code"].startswith("lab-method-"), m["code"]
        assert set(m["modes"]) <= set(rules["modes"]), m["code"]
        assert all(m.get(k) for k in ("name", "icon", "title", "persona")), m["code"]
        assert set(m.get("playbooks", [])) <= playbooks, m["code"]
    for mode, spec in rules["modes"].items():
        assert set(spec.get("methods", [])) <= set(codes), mode
    assert len({p["id"] for p in packs}) == len(packs)
    for pack in packs:
        assert pack["fields"] and set(pack["fields"]) <= set(rules["fos"]), pack["id"]
        assert pack["personas"], pack["id"]
        for persona in pack["personas"]:
            codes.append(persona["code"])
            assert persona["code"].startswith("pack-"), persona["code"]
            assert persona["slot"] in ("core", "skeptic", "translator"), persona["code"]
            assert all(persona.get(k) for k in ("name", "icon", "title", "persona")), persona["code"]
            assert set(persona.get("playbooks", [])) <= playbooks, persona["code"]
    assert len(codes) == len(set(codes)), "persona codes must be unique across the catalogue"
