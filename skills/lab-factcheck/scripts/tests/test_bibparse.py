import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bibparse  # noqa: E402

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


def test_bibparse_reads_braces_quotes_and_numbers():
    entries = bibparse.parse_bib(BIB)
    assert [e["key"] for e in entries] == ["garttner2018", "kasal2026sectors", "tang2019", "nodoi"]
    g = entries[0]["fields"]
    assert g["year"] == "2018" and g["volume"] == "120"
    assert "{multiple-quantum}" in g["title"]
    assert entries[1]["fields"]["author"] == 'Kasal, {\\"O}zcan'
