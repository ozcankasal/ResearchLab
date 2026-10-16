import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ledger  # noqa: E402

BIB = r"""
@comment{ignored}
@article{garttner2018,
  author  = {G{\"a}rttner, Martin and Hauke, Philipp and Rey, Ana Maria},
  title   = {Relating out-of-time-order correlations to entanglement via {multiple-quantum} coherences},
  journal = {Physical Review Letters},
  volume  = {120},
  pages   = {040402},
  year    = 2018,
  doi     = {10.1103/PhysRevLett.120.040402}
}
@misc{kasal2026sectors,
  author = "Kasal, {\"O}zcan",
  title  = "Fourier Sectors of Shifted Overlaps",
  note   = {Preprint, Zenodo, \url{https://doi.org/10.5281/zenodo.23137889}},
  year   = {2026}
}
@article{tang2019,
  author = {Tang, Ewin},
  title  = {A quantum-inspired classical algorithm for recommendation systems},
  year   = {2019},
  eprint = {1807.04271},
  archivePrefix = {arXiv}
}
@book{nodoi, author = {Someone}, title = {A Book}, year = {1999}}
"""

TEX_MAIN = r"""\documentclass{article}
\usepackage{thmtools}
\declaretheorem[name=Theorem]{theorem}
\declaretheorem[name=Proposition,sibling=theorem]{proposition}
\declaretheorem[style=remark,name=Remark]{remark}
\declaretheorem[name=Conjecture]{conjecture}
\begin{document}
This is the first result of its kind \cite{garttner2018,missingkey}. % first in a comment is ignored
\input{sec}
\end{document}
"""

TEX_SEC = r"""\begin{theorem}[Blindness]\label{thm:blind}
The kernels cannot see $W$.
\end{theorem}
\begin{proposition}
Unlabelled.
\end{proposition}
\begin{conjecture}\label{conj:var}
The variance grows like $\sqrt n$.
\end{conjecture}
\begin{remark}\label{rem:x} A remark. \end{remark}
We obviously win \citep[p.~3]{tang2019}.
"""


def test_ledger_finds_statements_citations_and_gaps(tmp_path):
    (tmp_path / "main.tex").write_text(TEX_MAIN, encoding="utf-8")
    (tmp_path / "sec.tex").write_text(TEX_SEC, encoding="utf-8")
    (tmp_path / "refs.bib").write_text(BIB, encoding="utf-8")
    with (tmp_path / "claims.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "kind", "evidence", "level", "checked_on", "notes"])
        writer.writerow(["thm:blind", "statement", "tests/test_winding.py", "CHECKED", "2026-10-16", ""])
        writer.writerow(["thm:gone", "statement", "", "PROVED", "", ""])
    with (tmp_path / "audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["key", "status"])
        writer.writerow(["garttner2018", "verified"])
        writer.writerow(["tang2019", "metadata only"])
    result = ledger.build(tmp_path / "main.tex", tmp_path / "refs.bib", tmp_path / "claims.csv", tmp_path / "audit.csv", False)
    envs = [s["env"] for s in result["statements"]]
    assert envs == ["theorem", "proposition", "conjecture"]
    assert result["statements"][0]["label"] == "thm:blind" and result["statements"][0]["file"] == "sec.tex"
    assert sorted({c["key"] for c in result["citations"]}) == ["garttner2018", "missingkey", "tang2019"]
    rules = [f["rule"] for f in result["findings"]]
    assert "unlabelled" in rules and "missing-bib" in rules and "orphan-row" in rules
    assert "no-audit" in rules and "audit-status" in rules and "uncited" in rules
    assert "no-evidence" in rules
    assert not result["ok"]
    words = {r["word"].lower() for r in result["review"]}
    assert {"first", "obviously"} <= words
    with_remarks = ledger.build(tmp_path / "main.tex", None, None, None, True)
    assert "remark" in [s["env"] for s in with_remarks["statements"]]


def test_ledger_level_rule(tmp_path):
    (tmp_path / "main.tex").write_text(TEX_MAIN.replace(r"\cite{garttner2018,missingkey}", ""), encoding="utf-8")
    (tmp_path / "sec.tex").write_text(TEX_SEC.replace("\\begin{proposition}\nUnlabelled.\n\\end{proposition}\n", ""), encoding="utf-8")
    with (tmp_path / "claims.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "kind", "evidence", "level", "checked_on", "notes"])
        writer.writerow(["thm:blind", "statement", "", "CONJECTURED", "", ""])
        writer.writerow(["conj:var", "statement", "", "CONJECTURED", "", ""])
    result = ledger.build(tmp_path / "main.tex", None, tmp_path / "claims.csv", None, False)
    assert [f["rule"] for f in result["findings"]] == ["level"]

