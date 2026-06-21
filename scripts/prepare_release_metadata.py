from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace(text: str, old: str, new: str) -> tuple[str, int]:
    count = text.count(old)
    return text.replace(old, new), count


def replace_regex(text: str, pattern: str, new: str) -> tuple[str, int]:
    updated, count = re.subn(pattern, new, text)
    return updated, count


def update_citation(text: str, repo_url: str, doi: str, release_date: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    text, count = replace_regex(text, r'repository-code:\s*".*?"', f'repository-code: "{repo_url}"')
    if count:
        changes.append("repository-code")
    text, count = replace_regex(text, r'date-released:\s*".*?"', f'date-released: "{release_date}"')
    if count:
        changes.append("date-released")
    if "doi:" in text:
        text, count = replace_regex(text, r'doi:\s*".*?"', f'doi: "{doi}"')
        if count:
            changes.append("doi")
    else:
        text = text.rstrip() + f'\ndoi: "{doi}"\n'
        changes.append("doi")
    return text, changes


def update_codemeta(text: str, repo_url: str, doi: str) -> tuple[str, list[str]]:
    data = json.loads(text)
    changes: list[str] = []
    if data.get("codeRepository") != repo_url:
        data["codeRepository"] = repo_url
        changes.append("codeRepository")
    identifier = f"https://doi.org/{doi}"
    if data.get("identifier") != identifier:
        data["identifier"] = identifier
        changes.append("identifier")
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n", changes


def update_zenodo(text: str, repo_url: str, doi: str) -> tuple[str, list[str]]:
    data = json.loads(text)
    changes: list[str] = []
    related = data.setdefault("related_identifiers", [])
    filtered_related = [
        item
        for item in related
        if not (item.get("scheme") == "doi" and item.get("relation") == "isIdenticalTo")
    ]
    if len(filtered_related) != len(related):
        data["related_identifiers"] = filtered_related
        related = filtered_related
        changes.append("related_identifiers.doi.replace")
    repo_entry = {
        "identifier": repo_url,
        "relation": "isSupplementTo",
        "scheme": "url",
    }
    if repo_entry not in related:
        related.append(repo_entry)
        changes.append("related_identifiers.repository")
    doi_entry = {
        "identifier": doi,
        "relation": "isIdenticalTo",
        "scheme": "doi",
    }
    if doi_entry not in related:
        related.append(doi_entry)
        changes.append("related_identifiers.doi")
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n", changes


def update_markdown(text: str, repo_url: str, doi: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    replacements = {
        "Pending public GitHub repository": repo_url,
        "Repository and DOI information will be finalized at release time.": (
            f"Repository: {repo_url}. Archived release DOI: {doi}."
        ),
        "Repository URL, archived DOI, and release metadata will be finalized at release time.": (
            f"Repository: {repo_url}. Archived release DOI: {doi}."
        ),
        "A Zenodo DOI is still a\nrelease-stage task.": f"Archived release DOI: {doi}.",
        "The archived Zenodo\nDOI will be added before SoftwareX submission.": f"Archived release DOI: {doi}.",
        "A Zenodo\nDOI archive will be added before SoftwareX submission.": f"Archived release DOI: {doi}.",
    }
    for old, new in replacements.items():
        text, count = replace(text, old, new)
        if count:
            changes.append(old[:40])
    text, count = replace_regex(
        text,
        r"The v[0-9]+\.[0-9]+\.[0-9]+ archived release DOI will be finalized after Zenodo processes the v[0-9]+\.[0-9]+\.[0-9]+ GitHub release\.",
        f"Archived release DOI: {doi}.",
    )
    if count:
        changes.append("pending release doi")
    text, count = replace_regex(text, r"Archived release DOI:\s*10\.5281/zenodo\.\d+\.", f"Archived release DOI: {doi}.")
    if count:
        changes.append("replace archived doi")
    if doi not in text and "Archived release DOI" not in text:
        text = text.rstrip() + f"\n\nArchived release DOI: {doi}.\n"
        changes.append("append doi")
    return text, changes


def update_tex(text: str, repo_url: str, doi: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    replacements = {
        "Pending public GitHub repository": repo_url,
        "Repository URL, archived DOI, and release metadata will be finalized at release\ntime.": (
            f"Repository: {repo_url}. Archived release DOI: {doi}."
        ),
        "The archived Zenodo DOI\nwill be added before SoftwareX submission.": f"Archived release DOI: {doi}.",
    }
    for old, new in replacements.items():
        text, count = replace(text, old, new)
        if count:
            changes.append(old[:40])
    text, count = replace_regex(
        text,
        r"The v[0-9]+\.[0-9]+\.[0-9]+\s+archived release DOI will be finalized after Zenodo processes the v[0-9]+\.[0-9]+\.[0-9]+ GitHub\s+release\.",
        f"Archived release DOI: {doi}.",
    )
    if count:
        changes.append("pending release doi")
    text, count = replace_regex(text, r"Archived release DOI:\s*10\.5281/zenodo\.\d+\.", f"Archived release DOI: {doi}.")
    if count:
        changes.append("replace archived doi")
    if doi not in text and "Archived release DOI" not in text:
        text = text.replace("\\end{document}", f"Archived release DOI: {doi}.\n\n\\end{{document}}")
        changes.append("append doi")
    return text, changes


def update_file(path_str: str, updater, apply: bool) -> dict[str, Any]:
    path = ROOT / path_str
    before = read(path)
    after, changes = updater(before)
    if apply and after != before:
        write(path, after)
    return {
        "path": path_str,
        "changed": after != before,
        "applied": apply and after != before,
        "changes": changes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare release metadata after public GitHub and Zenodo release.")
    parser.add_argument("--repo-url", required=True, help="Public GitHub repository URL.")
    parser.add_argument("--doi", required=True, help="Published Zenodo DOI, for example 10.5281/zenodo.1234567.")
    parser.add_argument("--release-date", required=True, help="Release date in YYYY-MM-DD format.")
    parser.add_argument("--apply", action="store_true", help="Write changes. Omit for dry-run.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.release_date):
        parser.error("--release-date must use YYYY-MM-DD")
    if not args.repo_url.startswith("https://github.com/"):
        parser.error("--repo-url must be a public GitHub HTTPS URL")
    if not args.doi.startswith("10."):
        parser.error("--doi must look like a DOI starting with 10.")

    updates = [
        update_file("CITATION.cff", lambda text: update_citation(text, args.repo_url, args.doi, args.release_date), args.apply),
        update_file("codemeta.json", lambda text: update_codemeta(text, args.repo_url, args.doi), args.apply),
        update_file(".zenodo.json", lambda text: update_zenodo(text, args.repo_url, args.doi), args.apply),
        update_file("README.md", lambda text: update_markdown(text, args.repo_url, args.doi), args.apply),
        update_file("paper/softwarex_manuscript.md", lambda text: update_markdown(text, args.repo_url, args.doi), args.apply),
        update_file("paper/softwarex_manuscript.tex", lambda text: update_tex(text, args.repo_url, args.doi), args.apply),
        update_file("paper/declarations.md", lambda text: update_markdown(text, args.repo_url, args.doi), args.apply),
    ]
    result = {"mode": "apply" if args.apply else "dry-run", "updates": updates}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"release metadata preparation: {result['mode']}")
        for item in updates:
            status = "APPLIED" if item["applied"] else "WOULD_CHANGE" if item["changed"] else "UNCHANGED"
            print(f"- {status}: {item['path']} ({', '.join(item['changes']) or 'no changes'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
