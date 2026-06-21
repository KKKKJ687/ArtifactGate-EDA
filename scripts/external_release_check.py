from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run_command(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def add_check(checks: list[dict[str, Any]], name: str, status: str, detail: str) -> None:
    checks.append({"name": name, "status": status, "detail": detail})


def parse_origin_repo() -> str | None:
    code, out, _ = run_command(["git", "remote", "get-url", "origin"])
    if code != 0 or not out:
        return None
    match = re.search(r"github\.com[:/](?P<owner>[^/\s]+)/(?P<repo>[^/\s]+?)(?:\.git)?$", out)
    if not match:
        return None
    return f"{match.group('owner')}/{match.group('repo')}"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fetch_json(url: str, timeout: int = 20) -> tuple[dict[str, Any] | None, str | None]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ArtifactGate-EDA external release checker",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, str(exc)


def check_local_metadata(checks: list[dict[str, Any]], doi: str | None) -> None:
    citation = read("CITATION.cff")
    codemeta = read("codemeta.json")
    manuscript = read("paper/softwarex_manuscript.md")

    placeholders = []
    for label, text in [
        ("CITATION.cff", citation),
        ("codemeta.json", codemeta),
        ("paper/softwarex_manuscript.md", manuscript),
    ]:
        if "<user>" in text or "2026-XX-XX" in text or "Pending public GitHub" in text:
            placeholders.append(label)
    if placeholders:
        add_check(checks, "metadata_placeholders", "BLOCKED", ", ".join(placeholders))
    else:
        add_check(checks, "metadata_placeholders", "PASS", "no release placeholders found")

    if doi:
        missing = [path for path, text in [("CITATION.cff", citation), ("paper/softwarex_manuscript.md", manuscript)] if doi not in text]
        if missing:
            add_check(checks, "doi_recorded", "BLOCKED", f"{doi} missing from {', '.join(missing)}")
        else:
            add_check(checks, "doi_recorded", "PASS", doi)
    else:
        add_check(checks, "doi_recorded", "BLOCKED", "provide --doi after Zenodo publication")


def check_public_doi(checks: list[dict[str, Any]], doi: str | None, repo: str | None) -> None:
    if not doi:
        return

    match = re.fullmatch(r"10\.5281/zenodo\.(?P<record_id>\d+)", doi)
    if not match:
        add_check(checks, "zenodo_record", "BLOCKED", f"{doi} is not a Zenodo DOI in 10.5281/zenodo.<id> form")
        return

    record_id = match.group("record_id")
    record, error = fetch_json(f"https://zenodo.org/api/records/{record_id}")
    if error or record is None:
        add_check(checks, "zenodo_record", "BLOCKED", error or f"Zenodo record {record_id} is not readable")
        return

    record_doi = record.get("doi")
    if record_doi != doi:
        add_check(checks, "zenodo_record", "BLOCKED", f"record DOI is {record_doi!r}, expected {doi}")
        return

    metadata = record.get("metadata") or {}
    title = metadata.get("title") or ""
    repo_url = f"https://github.com/{repo}" if repo else ""
    searchable = json.dumps(metadata, sort_keys=True)
    if "ArtifactGate-EDA" not in title and repo_url not in searchable:
        add_check(
            checks,
            "zenodo_record",
            "BLOCKED",
            f"Zenodo record {record_id} does not reference ArtifactGate-EDA or {repo_url}",
        )
        return

    url = (record.get("links") or {}).get("self_html", f"https://zenodo.org/records/{record_id}")
    add_check(checks, "zenodo_record", "PASS", f"{url} ({title})")


def check_local_artifacts(checks: list[dict[str, Any]]) -> None:
    required = [
        "release/artifactgate_eda_supplementary_artifacts.zip",
        "release/ngspice_minimal_artifactgate.zip",
        "release/hdl_icarus_artifactgate.zip",
        "release/yosys_artifactgate.zip",
        "dist/artifactgate_eda-0.1.1.tar.gz",
        "dist/artifactgate_eda-0.1.1-py3-none-any.whl",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    if missing:
        add_check(checks, "local_release_artifacts", "BLOCKED", ", ".join(missing))
    else:
        add_check(checks, "local_release_artifacts", "PASS", "release zips and Python dist files exist")


def check_github(checks: list[dict[str, Any]], repo: str | None, tag: str) -> None:
    if shutil.which("gh") is None:
        add_check(checks, "gh_cli", "BLOCKED", "gh CLI is not installed")
        return
    code, _, err = run_command(["gh", "auth", "status"])
    if code != 0:
        add_check(checks, "gh_auth", "BLOCKED", err or "gh auth status failed")
        return
    add_check(checks, "gh_auth", "PASS", "gh CLI is authenticated")

    if not repo:
        add_check(checks, "github_repository", "BLOCKED", "provide --repo owner/name or configure origin")
        return

    code, out, err = run_command(
        ["gh", "repo", "view", repo, "--json", "nameWithOwner,isPrivate,defaultBranchRef,url"]
    )
    if code != 0:
        add_check(checks, "github_repository", "BLOCKED", err or out)
        return
    repo_info = json.loads(out)
    if repo_info.get("isPrivate"):
        add_check(checks, "github_repository", "BLOCKED", f"{repo} is private")
    else:
        add_check(checks, "github_repository", "PASS", repo_info.get("url", repo))

    code, out, err = run_command(
        [
            "gh",
            "run",
            "list",
            "--repo",
            repo,
            "--branch",
            "main",
            "--limit",
            "1",
            "--json",
            "conclusion,status,workflowName,url,headSha",
        ]
    )
    if code != 0:
        add_check(checks, "github_actions", "BLOCKED", err or out)
    else:
        runs = json.loads(out)
        if runs and runs[0].get("status") == "completed" and runs[0].get("conclusion") == "success":
            add_check(checks, "github_actions", "PASS", runs[0].get("url", "latest run passed"))
        else:
            add_check(checks, "github_actions", "BLOCKED", json.dumps(runs[:1], sort_keys=True))

    code, out, err = run_command(["gh", "release", "view", tag, "--repo", repo, "--json", "tagName,url,isDraft"])
    if code != 0:
        add_check(checks, "github_release", "BLOCKED", err or out)
    else:
        release = json.loads(out)
        if release.get("isDraft"):
            add_check(checks, "github_release", "BLOCKED", f"{tag} is still a draft")
        else:
            add_check(checks, "github_release", "PASS", release.get("url", tag))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check external release gates for ArtifactGate-EDA.")
    parser.add_argument("--repo", help="GitHub repository in owner/name form. Defaults to origin when available.")
    parser.add_argument("--tag", default="v0.1.1")
    parser.add_argument("--doi", help="Published Zenodo DOI to verify in release metadata.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo = args.repo or parse_origin_repo()
    checks: list[dict[str, Any]] = []
    check_local_artifacts(checks)
    check_local_metadata(checks, args.doi)
    check_public_doi(checks, args.doi, repo)
    check_github(checks, repo, args.tag)

    blocked = [check for check in checks if check["status"] == "BLOCKED"]
    result = {"ok": not blocked, "status": "PASS" if not blocked else "BLOCKED", "repo": repo, "checks": checks}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"external release check: {result['status']}")
        for check in checks:
            print(f"- {check['status']}: {check['name']} - {check['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
