#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""refcheck: check every entry of a .bib file against Crossref (by DOI) and arXiv (by eprint id).

Usage:
  refcheck.py <references.bib> [--keys k1,k2] [--offline] [--cache <file.json>] [--sleep 0.3]
              [--format json|markdown]

For each entry it lints the record (title, author, year present; duplicate keys and DOIs), then, unless
--offline, fetches the DOI's record (Crossref, or DataCite for DOIs Crossref does not hold, such as
Zenodo's) and the arXiv record, and compares title (similarity), first author's family name, year, and
volume and pages when both sides have them. When a DOI record matches, differences from the arXiv
posting (titles and years often change on publication) are reported as notes, not mismatches. --cache stores fetched records as
JSON and is read first, so reruns and tests make no network calls.

Network: comparing metadata needs the registries, so the script queries Crossref and arXiv over HTTPS;
--offline lints without any call, and --cache makes reruns and tests offline.
Requests carry a neutral User-Agent and no personal data: no names or emails in headers, queries or URLs.

A "match" means the metadata agrees with the registry. That is METADATA-ONLY evidence: it does not show
that the source says what the citing sentence claims; reading the source does.

Output: JSON {"ok", "summary", "entries": [{"key", "status", "doi", "eprint", "issues", "registry"}]}
or a Markdown table. Statuses: match, mismatch, not-found, no-identifier, error, skipped (offline).
Exit 0 when no entry is mismatch, not-found or error; 1 otherwise; 2 on a usage error.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True  # the lab source stays read-only when linked into a project
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bibparse import parse_bib  # noqa: E402

USER_AGENT = "lab-refcheck/1.0 (bibliography metadata check)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s{}\"<>]+", re.IGNORECASE)
ARXIV_RE = re.compile(r"(?:arxiv[:/ ]\s*)?(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", re.IGNORECASE)


def fold(text: str) -> str:
    """Drop accents, both LaTeX-style ({\\"a}) and Unicode (ä), so names compare equal."""
    text = re.sub(r"\\[\"'`^~=.]\s*", "", text)
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def normalize_title(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)  # MathML and other markup in registry titles
    text = fold(text)
    text = re.sub(r"\\[a-zA-Z]+\s*", " ", text)
    text = re.sub(r"[{}$\\^_~\"'`]", "", text)
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def first_family_name(authors: str) -> str:
    first = re.split(r"\s+and\s+", authors.strip(), maxsplit=1)[0]
    first = re.sub(r"[{}\\'\"`^~]", "", first)
    family = first.split(",")[0] if "," in first else first.split()[-1] if first.split() else ""
    return family.strip().lower()


def identifiers(fields: dict[str, str]) -> tuple[str | None, str | None]:
    doi = None
    for name in ("doi", "url", "note", "howpublished"):
        m = DOI_RE.search(fields.get(name, ""))
        if m:
            doi = m.group(0).rstrip(".,;")
            break
    eprint = None
    if fields.get("eprint"):
        m = ARXIV_RE.search(fields["eprint"])
        eprint = m.group(1) if m else fields["eprint"].strip()
    else:
        for name in ("journal", "note", "url", "howpublished"):
            value = fields.get(name, "")
            if "arxiv" in value.lower():
                m = ARXIV_RE.search(value)
                if m:
                    eprint = m.group(1)
                    break
    return doi, eprint


def _get(url: str, accept: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def fetch_crossref(doi: str) -> dict | None:
    try:
        data = json.loads(_get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""), "application/json"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    message = data["message"]
    date = (message.get("published-print") or message.get("published-online") or message.get("issued") or {}).get("date-parts", [[None]])
    return {
        "source": "crossref",
        "title": (message.get("title") or [""])[0],
        "families": [a.get("family", "") for a in message.get("author", [])],
        "year": date[0][0] if date and date[0] else None,
        "container": (message.get("container-title") or [""])[0],
        "volume": message.get("volume"),
        "pages": message.get("page") or message.get("article-number"),
    }


def fetch_datacite(doi: str) -> dict | None:
    try:
        data = json.loads(_get("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe=""), "application/vnd.api+json"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    attributes = data["data"]["attributes"]
    return {
        "source": "datacite",
        "title": (attributes.get("titles") or [{}])[0].get("title", ""),
        "families": [c.get("familyName") or c.get("name", "").split(",")[0] for c in attributes.get("creators", [])],
        "year": attributes.get("publicationYear"),
        "container": attributes.get("publisher"),
        "volume": None,
        "pages": None,
    }


def parse_arxiv_atom(xml_text: bytes | str) -> dict | None:
    root = ET.fromstring(xml_text)
    entry = root.find(f"{ATOM}entry")
    if entry is None or entry.find(f"{ATOM}title") is None:
        return None
    entry_id = entry.findtext(f"{ATOM}id") or ""
    if "api/errors" in entry_id:
        return None
    published = entry.findtext(f"{ATOM}published") or ""
    return {
        "source": "arxiv",
        "title": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}title") or "").strip(),
        "families": [(a.findtext(f"{ATOM}name") or "").split()[-1] for a in entry.findall(f"{ATOM}author") if a.findtext(f"{ATOM}name")],
        "year": int(published[:4]) if published[:4].isdigit() else None,
        "doi": entry.findtext(f"{ARXIV}doi"),
        "journal_ref": entry.findtext(f"{ARXIV}journal_ref"),
    }


def fetch_arxiv(eprint: str) -> dict | None:
    return parse_arxiv_atom(_get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(eprint), "application/atom+xml"))


def same_family(ours: str, theirs: str) -> bool:
    """Equal, or one ends with the other: 'van den nest' and 'nest' name the same person."""
    return ours == theirs or ours.endswith(" " + theirs) or theirs.endswith(" " + ours) or ours.replace(" ", "") == theirs.replace(" ", "")


def compare(fields: dict[str, str], record: dict) -> list[str]:
    issues: list[str] = []
    ours = normalize_title(fields.get("title", ""))
    theirs = normalize_title(record.get("title", ""))
    ratio = difflib.SequenceMatcher(None, ours, theirs).ratio() if ours and theirs else 0.0
    if ratio < 0.9:
        issues.append(f"title differs (similarity {ratio:.2f}): registry has {record.get('title')!r}")
    family = normalize_title(first_family_name(fields.get("author", "")))
    families = [normalize_title(f) for f in record.get("families", []) if f]
    if family and families and not same_family(family, families[0]):
        issues.append(f"first author {family!r} differs: registry has {record['families'][0]!r}")
    year = fields.get("year", "").strip()
    if year.isdigit() and record.get("year") and int(year) != int(record["year"]):
        level = "year differs from the arXiv posting (fine if the journal year is cited)" if record["source"] == "arxiv" else "year differs"
        issues.append(f"{level}: bib {year}, registry {record['year']}")
    if record["source"] in ("crossref", "datacite"):
        if fields.get("volume") and record.get("volume") and fields["volume"].strip() != str(record["volume"]).strip():
            issues.append(f"volume differs: bib {fields['volume']}, registry {record['volume']}")
        bib_pages = re.sub(r"[-–—]+", "-", fields.get("pages", "")).strip()
        reg_pages = re.sub(r"[-–—]+", "-", str(record.get("pages") or "")).strip()
        if bib_pages and reg_pages and bib_pages.split("-")[0] != reg_pages.split("-")[0]:
            issues.append(f"pages differ: bib {fields['pages']}, registry {record['pages']}")
    return issues


def cached(cache: dict, kind: str, ident: str, fetch, sleep: float) -> dict | None:
    key = f"{kind}:{ident.lower()}"
    if key not in cache:
        cache[key] = fetch(ident)
        time.sleep(sleep)
    return cache[key]


def check(entries: list[dict], offline: bool, cache: dict, sleep: float) -> list[dict]:
    results = []
    seen_keys: set[str] = set()
    seen_dois: dict[str, str] = {}
    for entry in entries:
        fields = entry["fields"]
        doi, eprint = identifiers(fields)
        issues = []
        for name in ("title", "author", "year"):
            if not fields.get(name):
                issues.append(f"missing {name}")
        if entry["key"] in seen_keys:
            issues.append("duplicate key")
        seen_keys.add(entry["key"])
        if doi:
            if doi.lower() in seen_dois:
                issues.append(f"same DOI as {seen_dois[doi.lower()]}")
            seen_dois.setdefault(doi.lower(), entry["key"])
        result = {"key": entry["key"], "line": entry["line"], "doi": doi, "eprint": eprint, "issues": issues, "registry": []}
        if not doi and not eprint:
            result["status"] = "no-identifier"
            results.append(result)
            continue
        if offline:
            result["status"] = "skipped"
            results.append(result)
            continue
        status = "match"
        notes: list[str] = []
        doi_matched = False
        try:
            lookups = []
            if doi:
                lookups.append(("doi", doi))
            if eprint:
                lookups.append(("arxiv", eprint))
            for kind, ident in lookups:
                if kind == "doi":
                    record = cached(cache, "crossref", ident, fetch_crossref, sleep)
                    if record is None:
                        record = cached(cache, "datacite", ident, fetch_datacite, sleep)
                else:
                    record = cached(cache, "arxiv", ident, fetch_arxiv, sleep)
                if record is None:
                    issues.append(f"{'no DOI record (Crossref, DataCite)' if kind == 'doi' else 'arXiv has no record'} for {ident}")
                    status = "not-found"
                    continue
                result["registry"].append(record)
                found = compare(fields, record)
                if kind == "arxiv" and doi_matched:
                    notes.extend(f"arxiv: {text}" for text in found)
                    continue
                issues.extend(f"{record['source']}: {text}" for text in found if not text.startswith("year differs from the arXiv"))
                notes.extend(f"{record['source']}: {text}" for text in found if text.startswith("year differs from the arXiv"))
                if any(not text.startswith("year differs from the arXiv") for text in found):
                    if status == "match":
                        status = "mismatch"
                elif kind == "doi":
                    doi_matched = True
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError, KeyError) as error:
            status = "error"
            issues.append(f"lookup failed: {error}")
        result["notes"] = notes
        result["status"] = status
        results.append(result)
    return results


def markdown(results: list[dict]) -> str:
    lines = ["| Key | Status | Identifier | Issues | Notes |", "|---|---|---|---|---|"]
    for r in results:
        ident = r["doi"] or (f"arXiv:{r['eprint']}" if r["eprint"] else "-")
        lines.append(f"| {r['key']} | {r['status']} | {ident} | {'; '.join(r['issues']) or '-'} | {'; '.join(r.get('notes', [])) or '-'} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check .bib entries against Crossref and arXiv.")
    parser.add_argument("bib", type=Path)
    parser.add_argument("--keys")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--sleep", type=float, default=0.3)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    if not args.bib.is_file():
        print(f"error: {args.bib} is not a file", file=sys.stderr)
        return 2
    try:
        entries = parse_bib(args.bib.read_text(encoding="utf-8"))
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.keys:
        wanted = {k.strip() for k in args.keys.split(",")}
        entries = [e for e in entries if e["key"] in wanted]
    cache = json.loads(args.cache.read_text(encoding="utf-8")) if args.cache and args.cache.is_file() else {}
    results = check(entries, args.offline, cache, args.sleep)
    if args.cache:
        args.cache.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")
    bad = [r for r in results if r["status"] in ("mismatch", "not-found", "error")]
    summary = {status: sum(1 for r in results if r["status"] == status) for status in sorted({r["status"] for r in results})}
    if args.format == "markdown":
        print(markdown(results))
    else:
        print(json.dumps({"ok": not bad, "summary": summary, "entries": results}, indent=2, ensure_ascii=False))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
