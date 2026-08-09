"""Keyless SEC EDGAR client: fetch a 10-K's XBRL and shape it like sec-api's xbrl_to_json.

Data comes straight from sec.gov (no API key, User-Agent required):
  - ticker -> CIK:      https://www.sec.gov/files/company_tickers.json
  - CIK -> filings:     https://data.sec.gov/submissions/CIK##########.json
  - filing artifacts:   https://www.sec.gov/Archives/edgar/data/<cik>/<accession>/

The output dict is grouped by financial statement (CoverPage, StatementsOfIncome,
StatementsOfComprehensiveIncome, BalanceSheets, ...) with sec-api-compatible fact
entries: {"period": {...}, "segment": {...}?, "value": "..."} — the shape both
utils.get_income and the Rust models consume.
"""

import gzip
import json
import logging
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

logger = logging.getLogger(__name__)

USER_AGENT = "financial-analysis nick@advin.io"

_LINK = "{http://www.xbrl.org/2003/linkbase}"
_XLINK = "{http://www.w3.org/1999/xlink}"
_XBRLI = "{http://www.xbrl.org/2003/instance}"
_XBRLDI = "{http://xbrl.org/2006/xbrldi}"
_XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"

# Canonical sec-api statement keys, matched against the role URI's last path
# segment. Order matters: ComprehensiveIncome must win before the Income rule.
_STATEMENT_PATTERNS = [
    ("CoverPage", r"cover|documentandentityinformation"),
    ("StatementsOfComprehensiveIncome", r"comprehensiveincome"),
    (
        "StatementsOfIncome",
        r"statement.*(income|operations|earnings)|(income|operations|earnings).*statement",
    ),
    ("BalanceSheets", r"balancesheet|financialposition"),
]

_ticker_cache: dict[str, int] = {}


def _get(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
        if response.info().get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
    return data


def _get_json(url: str) -> dict:
    return json.loads(_get(url))


def get_cik(ticker: str) -> int:
    if not _ticker_cache:
        listing = _get_json("https://www.sec.gov/files/company_tickers.json")
        for entry in listing.values():
            _ticker_cache[entry["ticker"].lower()] = int(entry["cik_str"])
    cik = _ticker_cache.get(ticker.lower())
    if cik is None:
        raise ValueError(f"Ticker {ticker!r} not found in SEC company list")
    return cik


def find_10k(cik: int, year: int) -> dict:
    """Locate the 10-K whose fiscal period ends in `year`."""
    submissions = _get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    recent = submissions["filings"]["recent"]
    for i, form in enumerate(recent["form"]):
        report_date = recent["reportDate"][i]
        if form == "10-K" and report_date[:4] == str(year):
            return {
                "accession": recent["accessionNumber"][i],
                "primaryDocument": recent["primaryDocument"][i],
                "reportDate": report_date,
            }
    raise ValueError(f"No 10-K found for CIK {cik} with fiscal year {year}")


def filing_directory(cik: int, accession: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace('-', '')}"


def _find_xbrl_files(directory_url: str) -> tuple[str, str]:
    """Return (instance, presentation) file names from the filing directory.

    Some filers ship a standalone presentation linkbase (*_pre.xml); others
    (e.g. Workiva-produced filings) embed every linkbase inside the taxonomy
    schema (*.xsd), which _parse_presentation handles identically.
    """
    index = _get_json(f"{directory_url}/index.json")
    names = [item["name"] for item in index["directory"]["item"]]
    instance = next((n for n in names if n.endswith("_htm.xml")), None)
    presentation = next((n for n in names if n.endswith("_pre.xml")), None) or next(
        (n for n in names if n.endswith(".xsd")), None
    )
    if instance is None or presentation is None:
        raise ValueError(f"No XBRL instance/presentation found in {directory_url}")
    return instance, presentation


def _role_to_key(role_uri: str) -> str | None:
    segment = role_uri.rstrip("/").rsplit("/", 1)[-1].lower()
    for key, pattern in _STATEMENT_PATTERNS:
        if re.search(pattern, segment):
            if "parenthetical" in segment:
                return key + "Parenthetical"
            return key
    return None


def _parse_presentation(xml_bytes: bytes) -> dict[str, list[str]]:
    """Map each statement key to the concept local names it presents, in order."""
    statements: dict[str, list[str]] = {}
    root = ET.fromstring(xml_bytes)
    for link in root.iter(_LINK + "presentationLink"):
        key = _role_to_key(link.get(_XLINK + "role", ""))
        if key is None:
            continue
        concepts = statements.setdefault(key, [])
        seen = set(concepts)
        for loc in link.iter(_LINK + "loc"):
            fragment = loc.get(_XLINK + "href", "").rsplit("#", 1)[-1]
            if "_" not in fragment:
                continue
            name = fragment.split("_", 1)[1]
            if name not in seen:
                seen.add(name)
                concepts.append(name)
    return statements


def _parse_instance(xml_bytes: bytes) -> tuple[dict, dict]:
    """Extract contexts (periods + dimension segments) and facts by concept name."""
    contexts: dict[str, dict] = {}
    facts: dict[str, list[dict]] = {}
    root = ET.fromstring(xml_bytes)

    for context in root.iter(_XBRLI + "context"):
        period: dict[str, str] = {}
        period_el = context.find(_XBRLI + "period")
        if period_el is not None:
            for child in period_el:
                tag = child.tag.rsplit("}", 1)[-1]
                if tag == "instant":
                    period = {"instant": child.text or ""}
                else:  # startDate / endDate
                    period[tag] = child.text or ""
        segments = [
            {"dimension": member.get("dimension"), "value": (member.text or "").strip()}
            for member in context.iter(_XBRLDI + "explicitMember")
        ]
        contexts[context.get("id", "")] = {"period": period, "segments": segments}

    for element in root:
        context_ref = element.get("contextRef")
        if context_ref is None or element.get(_XSI_NIL) == "true":
            continue
        value = (element.text or "").strip()
        if not value:
            continue
        name = element.tag.rsplit("}", 1)[-1]
        fact = {"contextRef": context_ref, "value": value}
        # Numeric facts carry these; the Rust MetricValue model requires them.
        if element.get("decimals") is not None:
            fact["decimals"] = element.get("decimals")
        if element.get("unitRef") is not None:
            fact["unitRef"] = element.get("unitRef")
        facts.setdefault(name, []).append(fact)

    return contexts, facts


def _duration_days(period: dict) -> int:
    try:
        start = date.fromisoformat(period["startDate"])
        end = date.fromisoformat(period["endDate"])
    except (KeyError, ValueError):
        return 0
    return (end - start).days


def _entry_sort_key(entry: dict) -> tuple:
    # Consolidated (no segment) first, then longest duration, then latest period —
    # get_gaap_period_int takes the first entry matching the requested year, so the
    # annual consolidated fact must precede quarterly and segmented ones.
    period = entry["period"]
    return (
        "segment" in entry,
        -_duration_days(period),
        period.get("endDate", period.get("instant", "")),
    )


def _build_filing_json(
    statements: dict[str, list[str]], contexts: dict, facts: dict
) -> dict:
    filing: dict[str, dict] = {}
    for key, concepts in statements.items():
        section: dict[str, list] = {}
        for concept in concepts:
            entries = []
            seen_entries = set()
            for fact in facts.get(concept, []):
                context = contexts.get(fact["contextRef"])
                if context is None:
                    continue
                period = context["period"]
                if "instant" in period:
                    period = {
                        "startDate": period["instant"],
                        "endDate": period["instant"],
                        "instant": period["instant"],
                    }
                entry: dict = {"period": period}
                segments = context["segments"]
                if segments:
                    entry["segment"] = segments[0] if len(segments) == 1 else segments
                for attr in ("decimals", "unitRef"):
                    if attr in fact:
                        entry[attr] = fact[attr]
                entry["value"] = fact["value"]
                # The same fact often appears under several contexts (statement +
                # note reuse); consumers that sum entries must see it only once.
                fingerprint = json.dumps(entry, sort_keys=True)
                if fingerprint in seen_entries:
                    continue
                seen_entries.add(fingerprint)
                entries.append(entry)
            if entries:
                entries.sort(key=_entry_sort_key)
                section[concept] = entries
        if section:
            filing[key] = section
    return filing


def get_filing_json(ticker: str, year: int) -> tuple[dict, str]:
    """Fetch the 10-K for `ticker` fiscal `year` as a statement-grouped dict.

    Returns (filing_json, primary_document_url).
    """
    cik = get_cik(ticker)
    filing = find_10k(cik, year)
    directory = filing_directory(cik, filing["accession"])
    instance_name, presentation_name = _find_xbrl_files(directory)
    logger.info("Fetching %s 10-K FY%s from %s", ticker.upper(), year, directory)

    statements = _parse_presentation(_get(f"{directory}/{presentation_name}"))
    contexts, facts = _parse_instance(_get(f"{directory}/{instance_name}"))
    filing_json = _build_filing_json(statements, contexts, facts)
    return filing_json, f"{directory}/{filing['primaryDocument']}"
