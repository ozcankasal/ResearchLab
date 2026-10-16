import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tells  # noqa: E402

# Fixture packs: test data only. Real packs are written per project by the lab-voice skill.
EN = r'''
[pack]
code = "en"
language = "English"
[detect]
words = ["the", "of", "and", "to", "a", "in", "is", "that", "it", "for", "on", "with", "as", "are", "this", "we", "by", "be", "not", "or"]
[categories.inflation]
patterns = ['\bpivotal\b', '\bcrucial\b', '\bdelve\w*', '\btapestry\b', '\bintricate\b', '\ba testament to\b', '\bpaves? the way\b', '\bunderscor\w+']
advice = "state the consequence"
[categories.copula]
patterns = ['\bserves? as\b', '\bboasts?\b']
[categories.trailing]
patterns = [',\s*(?:highlighting|underscoring|showcasing)\b']
[categories.authority]
patterns = ['\bexperts (?:argue|say)\b']
[categories.setpiece]
patterns = ['\bnot only\b[^.]{1,80}\bbut also\b']
[categories.signpost]
patterns = ['(?:Additionally|Moreover|Furthermore),']
sentence_initial = true
case_sensitive = true
[categories.closer]
patterns = ['(?:Overall|In summary),', 'This underscores']
sentence_initial = true
case_sensitive = true
[categories.hedge]
patterns = ['\bmay potentially\b']
[categories.throat]
patterns = ['\bin this paper, we delve\b', "\\blet's dive\\b"]
[examples]
positive = ["The winding serves as a testament to symmetry.", "Additionally, the kernel is blind.", "It may potentially help."]
negative = ["The kernels cannot see the phase.", "We found a pair whose kernels agree to 1e-17.", "The winding is 2 for one pair and 1 for its mirror."]
'''

DE = r'''
[pack]
code = "de"
language = "German"
[detect]
words = ["der", "die", "das", "und", "ist", "nicht", "ein", "eine", "zu", "den", "von", "mit", "sich", "des", "auf", "für", "im", "dem", "wir", "es"]
[categories.inflation]
patterns = ['\bvon entscheidender Bedeutung\b', '\bbahnbrechend\w*', '\bwegweisend\w*']
[categories.signpost]
patterns = ['(?:Darüber hinaus|Zudem|Des Weiteren),?']
sentence_initial = true
case_sensitive = true
[categories.setpiece]
patterns = ['\bnicht nur\b[^.]{1,80}\bsondern auch\b']
[examples]
positive = ["Das Ergebnis ist von entscheidender Bedeutung.", "Darüber hinaus ist die Methode bahnbrechend.", "Es ist nicht nur schnell, sondern auch genau."]
negative = ["Die Kerne sehen die Phase nicht.", "Wir haben zwölf Paare gemessen.", "Der Fehler liegt unter einem Prozent."]
'''

JA = r'''
[pack]
code = "ja"
language = "Japanese"
has_case = false
[detect]
words = ["の", "は", "が", "を", "に", "で", "と", "た", "です", "ます"]
[text]
sentence_end = "[。！？]"
unit = "char"
[categories.inflation]
patterns = ['極めて重要', '画期的']
[categories.signpost]
patterns = ['さらに、', 'また、']
sentence_initial = true
case_sensitive = true
[examples]
positive = ["この結果は極めて重要です。", "さらに、この方法は画期的です。", "画期的な成果を示した。"]
negative = ["位相は核に見えない。", "十二組を測定した。", "誤差は一パーセント未満だった。"]
'''

MACHINE = """# A Comprehensive Guide To Shift Windings

In this paper, we delve into the intricate tapestry of quantum overlaps. The winding serves as a testament to the pivotal role of phases, highlighting the importance of symmetry. Additionally, experts argue that it may potentially pave the way for new insights.

- **Invariance:** it is not only elegant but also exact.
- **Blindness:** kernels cannot see it 🚀

Overall, this underscores the significance of our approach — a crucial step.
"""

HUMAN = """# What the kernels miss

The sector kernels are built from the modulus of the shifted overlap. They cannot see its phase. For two states on three qubits we found a pair whose kernels agree to 1e-17 while the windings are 2 and 1. A mirror map explains it: complex conjugation followed by a global bit flip keeps every kernel and sends W to n - W.

Why does this matter? Because swap tests on a shift grid measure exactly the kernels. No amount of such data fixes W.
"""


def packs(tmp_path, *texts):
    folder = tmp_path / "packs"
    folder.mkdir(exist_ok=True)
    for text in texts:
        code = text.split('code = "')[1].split('"')[0]
        (folder / f"{code}.toml").write_text(text, encoding="utf-8")
    return folder


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_script_holds_no_language_vocabulary():
    source = Path(tells.__file__).read_text(encoding="utf-8")
    for word in ("delve", "pivotal", "Additionally", "kritik", "bağlamda"):
        assert word not in source


def test_pack_check_accepts_good_packs_and_rejects_bad_ones(tmp_path):
    folder = packs(tmp_path, EN, DE, JA)
    for code in ("en", "de", "ja"):
        report = tells.check_pack(folder / f"{code}.toml")
        assert report["ok"], report
    bad = EN.replace("\"It may potentially help.\"", "\"It helps.\"").replace("\"The kernels cannot see the phase.\"", "\"It is crucial.\"")
    report = tells.check_pack(write(tmp_path, "bad.toml", bad))
    assert not report["ok"]
    assert any("positive example triggers nothing" in e for e in report["errors"])
    assert any("negative example triggers" in e for e in report["errors"])
    broken = write(tmp_path, "broken.toml", EN.replace(r"'\bboasts?\b'", "'(unclosed'"))
    assert not tells.check_pack(broken)["ok"]


def test_auto_detection_picks_the_right_pack(tmp_path):
    folder = packs(tmp_path, EN, DE, JA)
    loaded = tells.load_packs(folder)
    german = write(tmp_path, "de.md", "Darüber hinaus ist die Methode bahnbrechend und die Ergebnisse sind von entscheidender Bedeutung für die Physik. " * 3)
    japanese = write(tmp_path, "ja.md", "さらに、この方法は画期的です。結果は極めて重要です。位相は核に見えない。" * 3)
    english = write(tmp_path, "en.md", MACHINE)
    assert tells.scan(german, loaded)["language"] == "de"
    assert tells.scan(japanese, loaded)["language"] == "ja"
    result = tells.scan(english, loaded)
    assert result["language"] == "en"
    cats = {f["category"] for f in result["findings"]}
    assert {"inflation", "copula", "trailing", "authority", "setpiece", "signpost", "closer", "hedge", "throat",
            "bold-lead", "title-case", "emoji", "em-dash"} <= cats


def test_japanese_counts_characters_and_skips_title_case(tmp_path):
    folder = packs(tmp_path, JA)
    text = "# 位相の話\n\nさらに、この方法は画期的です。結果は極めて重要です。十二組を測定した。誤差は一パーセント未満だった。\n"
    result = tells.scan(write(tmp_path, "j.md", text), tells.load_packs(folder))
    assert result["language"] == "ja" and result["cadence"]["unit"] == "char"
    assert {"signpost", "inflation"} <= {f["category"] for f in result["findings"]}
    assert "title-case" not in {f["category"] for f in result["findings"]}


def test_unknown_language_reports_a_profile_and_exit_3(tmp_path, capsys):
    folder = packs(tmp_path, EN)
    finnish = write(tmp_path, "fi.md", "Tämä tulos on erittäin tärkeä ja se osoittaa, että menetelmä toimii hyvin myös suurilla järjestelmillä. " * 4)
    assert tells.main([str(finnish), "--packs", str(folder)]) == 3
    out = json.loads(capsys.readouterr().out)
    assert out["language"] is None and out["profile"]["scripts"].get("LATIN")
    assert "ä" in out["profile"]["non_ascii_letters"] and "tulos" in out["profile"]["frequent_words"]


def test_neutral_checks_run_without_any_pack(tmp_path):
    result = tells.scan(write(tmp_path, "m.md", MACHINE), [], "none")
    cats = {f["category"] for f in result["findings"]}
    assert cats == {"bold-lead", "title-case", "emoji", "em-dash"}
    assert "profile" not in result


def test_human_text_is_quiet_and_varied(tmp_path):
    folder = packs(tmp_path, EN)
    result = tells.scan(write(tmp_path, "h.md", HUMAN), tells.load_packs(folder))
    assert result["language"] == "en" and result["density_per_1000"]["total"] == 0
    assert result["cadence"]["cv"] > 0.35


def test_latex_math_citations_and_table_dashes_are_ignored(tmp_path):
    folder = packs(tmp_path, EN)
    tex = r"""We prove the result \cite{crucial2020} for $\text{pivotal}$ cases and it is the one that we use in the paper. % crucial comment
\begin{equation}
  \mathrm{delve} = 1
\end{equation}
The kernel serves as a filter for the states of the register and it is not a projector.
"""
    result = tells.scan(write(tmp_path, "p.tex", tex), tells.load_packs(folder))
    assert [(f["line"], f["text"].lower()) for f in result["findings"]] == [(5, "serves as")]
    table = "| Phase | Room |\n|---|---|\n| Survey | — |\n\nThe result held — barely, and it is the one we use.\n"
    result = tells.scan(write(tmp_path, "t.md", table), tells.load_packs(folder))
    assert [f["line"] for f in result["findings"] if f["category"] == "em-dash"] == [5]


def test_cli_usage_errors_and_density_gate(tmp_path, capsys):
    folder = packs(tmp_path, EN)
    path = write(tmp_path, "m.md", MACHINE)
    assert tells.main([str(path), "--packs", str(folder), "--format", "markdown"]) == 0
    assert "| Habit | Per 1000 |" in capsys.readouterr().out
    assert tells.main([str(path), "--packs", str(folder), "--max-density", "5"]) == 1
    assert tells.main([str(path), "--packs", str(folder), "--lang", "xx"]) == 2
    assert tells.main([str(tmp_path / "missing.md")]) == 2
    assert tells.main(["--check-pack", str(folder / "en.toml")]) == 0
