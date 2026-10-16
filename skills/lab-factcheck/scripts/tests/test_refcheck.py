import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bibparse  # noqa: E402
import refcheck  # noqa: E402

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

ARXIV_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/1807.04271v3</id>
    <published>2018-07-10T17:59:58Z</published>
    <title>A quantum-inspired classical algorithm for recommendation
  systems</title>
    <author><name>Ewin Tang</name></author>
    <arxiv:doi>10.1145/3313276.3316310</arxiv:doi>
  </entry>
</feed>"""

def test_identifiers_find_doi_in_note_and_arxiv_eprint():
    entries = {e["key"]: e for e in bibparse.parse_bib(BIB)}
    assert refcheck.identifiers(entries["kasal2026sectors"]["fields"]) == ("10.5281/zenodo.23137889", None)
    assert refcheck.identifiers(entries["tang2019"]["fields"]) == (None, "1807.04271")
    assert refcheck.identifiers(entries["nodoi"]["fields"]) == (None, None)


def test_compare_flags_wrong_title_author_volume():
    fields = bibparse.parse_bib(BIB)[0]["fields"]
    good = {"source": "crossref", "title": "Relating Out-of-Time-Order Correlations to Entanglement via Multiple-Quantum Coherences",
            "families": ["Gärttner", "Hauke", "Rey"], "year": 2018, "volume": "120", "pages": "040402"}
    assert refcheck.compare(fields, good) == []
    bad = dict(good, title="Something else entirely", families=["Smith"], volume="121")
    issues = refcheck.compare(fields, bad)
    assert any("title" in i for i in issues) and any("first author" in i for i in issues) and any("volume" in i for i in issues)


def test_arxiv_atom_parsing():
    record = refcheck.parse_arxiv_atom(ARXIV_XML)
    assert record["title"] == "A quantum-inspired classical algorithm for recommendation systems"
    assert record["families"] == ["Tang"] and record["year"] == 2018


def test_check_with_cache_makes_no_network_calls(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(refcheck, "_get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    bib = tmp_path / "refs.bib"
    bib.write_text(BIB, encoding="utf-8")
    cache = tmp_path / "cache.json"
    cache.write_text(json.dumps({
        "crossref:10.1103/physrevlett.120.040402": {"source": "crossref", "title": "Relating out-of-time-order correlations to entanglement via multiple-quantum coherences", "families": ["Gärttner"], "year": 2018, "volume": "120", "pages": "040402"},
        "crossref:10.5281/zenodo.23137889": {"source": "crossref", "title": "Fourier Sectors of Shifted Overlaps", "families": ["Kasal"], "year": 2026, "volume": None, "pages": None},
        "arxiv:1807.04271": refcheck.parse_arxiv_atom(ARXIV_XML),
    }), encoding="utf-8")
    code = refcheck.main([str(bib), "--cache", str(cache)])
    out = json.loads(capsys.readouterr().out)
    statuses = {e["key"]: e["status"] for e in out["entries"]}
    assert statuses == {"garttner2018": "match", "kasal2026sectors": "match", "tang2019": "match", "nodoi": "no-identifier"}
    assert code == 0
    assert refcheck.main([str(bib), "--offline", "--format", "markdown"]) == 0
    assert "| tang2019 | skipped | arXiv:1807.04271 |" in capsys.readouterr().out


def test_user_agent_carries_no_personal_data():
    assert "@" not in refcheck.USER_AGENT and "mailto" not in refcheck.USER_AGENT


def test_registry_markup_and_particle_surnames():
    fields = {"title": "Characterizing correlations with full counting statistics: Classical Ising and quantum XY spin chains",
              "author": "van den Nest, Maarten", "year": "2013"}
    record = {"source": "crossref", "families": ["Nest"], "year": 2013, "volume": None, "pages": None,
              "title": 'Characterizing correlations with full counting statistics: Classical Ising and quantum<mml:math xmlns:mml="x"><mml:mi>X</mml:mi><mml:mi>Y</mml:mi></mml:math>spin chains'}
    assert refcheck.compare(fields, record) == []
    assert refcheck.same_family("van den nest", "nest") and not refcheck.same_family("nest", "west")


def test_zenodo_doi_falls_back_to_datacite_and_arxiv_differences_are_notes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(refcheck, "_get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    bib = tmp_path / "refs.bib"
    bib.write_text(r"""
@misc{zen, author = {Kasal, Ozcan}, title = {Fourier Sectors of Shifted Overlaps}, year = {2026}, doi = {10.5281/zenodo.1}}
@article{wei, author = {Wei, Bo-Bo and Liu, Ren-Bao}, title = {Lee-Yang zeros and critical times in decoherence of a probe spin coupled to a bath},
  journal = {PRL}, year = {2012}, doi = {10.1103/PhysRevLett.109.185701}, eprint = {1206.5442}}
""", encoding="utf-8")
    cache = tmp_path / "cache.json"
    cache.write_text(json.dumps({
        "crossref:10.5281/zenodo.1": None,
        "datacite:10.5281/zenodo.1": {"source": "datacite", "title": "Fourier Sectors of Shifted Overlaps", "families": ["Kasal"], "year": 2026, "volume": None, "pages": None},
        "crossref:10.1103/physrevlett.109.185701": {"source": "crossref", "title": "Lee-Yang Zeros and Critical Times in Decoherence of a Probe Spin Coupled to a Bath", "families": ["Wei", "Liu"], "year": 2012, "volume": None, "pages": None},
        "arxiv:1206.5442": {"source": "arxiv", "title": "Probing Lee-Yang zeros and coherence sudden death", "families": ["Wei", "Liu"], "year": 2012},
    }), encoding="utf-8")
    assert refcheck.main([str(bib), "--cache", str(cache)]) == 0
    out = json.loads(capsys.readouterr().out)
    entries = {e["key"]: e for e in out["entries"]}
    assert entries["zen"]["status"] == "match" and entries["zen"]["registry"][0]["source"] == "datacite"
    assert entries["wei"]["status"] == "match" and any("title differs" in n for n in entries["wei"]["notes"])
