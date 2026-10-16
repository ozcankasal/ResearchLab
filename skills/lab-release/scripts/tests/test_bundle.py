import json
import sys
import tarfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bundle  # noqa: E402


def project(tmp_path):
    root = tmp_path / "proj"
    for rel, text in {
        "README.md": "readme",
        "LICENSE": "MIT",
        "src/pkg/__init__.py": "x = 1\n",
        "tests/test_x.py": "def test_x():\n    assert True\n",
        "paper/main.tex": "\\documentclass{article}\n% TODO remove before posting\n\\begin{document}hi\\end{document}\n",
        "paper/references.bib": "",
        "paper/figures/fig1.pdf": "%PDF-1.4",
        "paper/main.pdf": "%PDF-1.4",
        "references/notes/a.md": "note",
        "references/pdf/a.pdf": "private",
    }.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def manifest(tmp_path, root, code_include):
    path = root / "release.toml"
    path.write_text(f"""
[release]
name = "proj"
version = "1.0"
out = "{(tmp_path / 'deposit').as_posix()}"

[pdf]
source = "paper/main.pdf"
name = "proj-{{version}}.pdf"

[source]
root = "paper"
main = "main.tex"
files = ["main.tex", "references.bib", "figures/*.pdf"]

[code]
include = {json.dumps(code_include)}
exclude = ["references/pdf/**"]
""", encoding="utf-8")
    return path


def test_build_writes_three_artifacts_and_flags_public_comments(tmp_path):
    root = project(tmp_path)
    path = manifest(tmp_path, root, ["README.md", "LICENSE", "src/**/*.py", "tests/*.py", "references/notes/*.md"])
    result = bundle.build(path, dry_run=False, verify="python -c \"import pathlib; assert pathlib.Path('src/pkg/__init__.py').exists()\"")
    assert result["ok"], result
    deposit = tmp_path / "deposit"
    assert (deposit / "proj-1.0.pdf").exists()
    with tarfile.open(deposit / "latex-source.tar.gz") as tar:
        assert sorted(tar.getnames()) == ["figures/fig1.pdf", "main.tex", "references.bib"]
    with zipfile.ZipFile(deposit / "proj-v1.0.zip") as zf:
        names = zf.namelist()
    assert "proj-v1.0/src/pkg/__init__.py" in names and not any("references/pdf" in n for n in names)
    assert any("comment will be public" in f["text"] for f in result["findings"])
    assert result["verify"]["ok"]


def test_private_files_and_dead_patterns_stop_the_build(tmp_path):
    root = project(tmp_path)
    (root / ".env").write_text("TOKEN=x", encoding="utf-8")
    path = manifest(tmp_path, root, ["references/**/*", ".env", "nothing/*.py"])
    path.write_text(path.read_text().replace('exclude = ["references/pdf/**"]', "exclude = []"), encoding="utf-8")
    result = bundle.build(path, dry_run=False, verify=None)
    texts = " ".join(f["text"] for f in result["findings"])
    assert not result["ok"]
    assert "private" in texts and "secret" in texts and "matches no file" in texts
    assert not (tmp_path / "deposit").exists()


def test_dry_run_and_cli(tmp_path, capsys):
    root = project(tmp_path)
    path = manifest(tmp_path, root, ["README.md"])
    assert bundle.main([str(path), "--dry-run", "--format", "markdown"]) == 0
    assert "| proj-v1.0.zip | code | 1 |" in capsys.readouterr().out
    assert not (tmp_path / "deposit").exists()
    assert bundle.main([str(tmp_path / "missing.toml")]) == 2
