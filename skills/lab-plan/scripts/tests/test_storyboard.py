import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import storyboard  # noqa: E402


def story(sid, kind, status="todo", deps="[]", claim="C1", ac=True):
    body = f"""---
id: {sid}
type: {kind}
title: Story {sid}
claim: {claim}   # the claim it serves
owner: lab-agent-methods
depends_on: {deps}
status: {status}
size: M
---
# {sid}
"""
    if ac:
        body += "\n## Acceptance criteria\n\n- something checkable\n"
    return body


def make_plan(tmp_path, stories):
    folder = tmp_path / "plan-x" / "stories"
    folder.mkdir(parents=True)
    for sid, text in stories.items():
        (folder / f"{sid}.md").write_text(text, encoding="utf-8")
    return tmp_path / "plan-x"


def test_ready_blocked_and_order(tmp_path):
    plan = make_plan(tmp_path, {
        "LEM-1": story("LEM-1", "LEM", status="done"),
        "THM-1": story("THM-1", "THM", deps="[LEM-1]"),
        "EXP-1": story("EXP-1", "EXP", deps="[THM-1]"),
        "LIT-1": story("LIT-1", "LIT", claim="-"),
    })
    result = storyboard.board(plan, None)
    assert result["ok"], result["findings"]
    assert result["ready"] == ["LIT-1", "THM-1"]
    assert result["blocked"] == ["EXP-1"]
    assert result["order"].index("LEM-1") < result["order"].index("THM-1") < result["order"].index("EXP-1")
    assert "LEM_1 --> THM_1" in result["mermaid"]


def test_errors_are_reported(tmp_path):
    plan = make_plan(tmp_path, {
        "THM-1": story("THM-1", "THM", deps="[THM-2]"),
        "THM-2": story("THM-2", "THM", deps="[THM-1]"),
        "EXP-1": story("EXP-1", "CODE"),
        "CODE-1": story("CODE-1", "CODE", deps="[NOPE-9]", ac=False),
        "LEM-1": story("LEM-1", "LEM", status="finished"),
    })
    result = storyboard.board(plan, None)
    rules = {f["rule"] for f in result["findings"]}
    assert not result["ok"]
    assert {"cycle", "id-type", "dependency", "acceptance", "status"} <= rules


def test_claims_checked_against_brief(tmp_path):
    plan = make_plan(tmp_path, {"THM-1": story("THM-1", "THM", claim="C7")})
    brief = tmp_path / "brief.md"
    brief.write_text("| C1 | a claim |\n| C2 | another |\n", encoding="utf-8")
    result = storyboard.board(plan, brief)
    assert any(f["rule"] == "claim" for f in result["findings"])


def test_cli_markdown_and_exit_codes(tmp_path, capsys):
    plan = make_plan(tmp_path, {"THM-1": story("THM-1", "THM")})
    assert storyboard.main([str(plan), "--format", "markdown"]) == 0
    out = capsys.readouterr().out
    assert "| THM-1: Story THM-1 | THM | C1 |" in out
    assert storyboard.main([str(plan)]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ready"] == ["THM-1"] and "_stories" not in data
    assert storyboard.main([str(tmp_path / "missing")]) == 2
