from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWLIST = [
    re.compile(r"Mert Gedik"),
    re.compile(r"MertGedik35"),
    re.compile(r"\d+\+MertGedik35@users\.noreply\.github\.com"),
    re.compile(r"\d+\+dependabot\[bot\]@users\.noreply\.github\.com"),
    re.compile(r"noreply@github\.com"),
    re.compile(r"example", re.IGNORECASE),
]

TURKISH_MOBILE_RE = r"(?<![\w])(?:\+90|0090|0)?[\s().-]*5\d{2}(?:[\s().-]*\d){7}(?!\d)"
INTERNATIONAL_PHONE_RE = r"(?<![\w])\+[1-9]\d{0,2}(?:[\s().-]*\d){7,12}(?!\d)"
GENERATED_VENDOR_SITE_DIRS = {
    Path("site/assets/javascripts"),
    Path("site/assets/stylesheets"),
}

PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(f"(?:{TURKISH_MOBILE_RE})|(?:{INTERNATIONAL_PHONE_RE})"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    "secret_token": re.compile(r"\b(?:sk|gho|ghp|xox[baprs])_[A-Za-z0-9_\-]{10,}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    "credential_assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]"
    ),
    "windows_home_path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
    "unix_home_path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
}


@dataclass
class Finding:
    category: str
    location: str
    value: str
    allowed: bool
    scope: str

    def redacted(self) -> str:
        if len(self.value) <= 8:
            return "<redacted>"
        return f"{self.value[:3]}...{self.value[-3:]}"


def is_allowed(value: str) -> bool:
    return any(pattern.search(value) for pattern in ALLOWLIST)


def tracked_files(include_site: bool) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
    )
    files = [ROOT / line for line in result.stdout.splitlines() if line.strip()]
    if include_site and (ROOT / "site").exists():
        files.extend(path for path in (ROOT / "site").rglob("*") if path.is_file())
    return files


def scan_text(text: str, location: str, scope: str) -> list[Finding]:
    findings: list[Finding] = []
    for category, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(0)
            findings.append(Finding(category, location, value, is_allowed(value), scope))
    return findings


def scan_files(include_site: bool) -> list[Finding]:
    findings: list[Finding] = []
    for path in tracked_files(include_site):
        if not path.exists():
            continue
        relative_path = path.relative_to(ROOT)
        if any(
            relative_path == excluded or excluded in relative_path.parents
            for excluded in GENERATED_VENDOR_SITE_DIRS
        ):
            continue
        if any(part in {".venv", ".git"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, str(relative_path), "current_tree"))
    return findings


def scan_git_metadata() -> list[Finding]:
    result = subprocess.run(
        ["git", "log", "--all", "--format=%H %an <%ae> | %cn <%ce>"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return scan_text(result.stdout, "git log --all author/committer metadata", "git_metadata")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-site", action="store_true")
    parser.add_argument("--include-git", action="store_true")
    parser.add_argument("--history-warn-only", action="store_true")
    args = parser.parse_args()
    findings = scan_files(include_site=args.include_site)
    if args.include_git:
        findings.extend(scan_git_metadata())
    unapproved = [
        finding
        for finding in findings
        if not finding.allowed and not (args.history_warn_only and finding.scope == "git_metadata")
    ]
    grouped: dict[str, int] = {}
    for finding in findings:
        key = f"{finding.scope}:{finding.category}:{'allowed' if finding.allowed else 'unapproved'}"
        grouped[key] = grouped.get(key, 0) + 1
    print("Privacy audit summary")
    print(json.dumps(grouped, indent=2, sort_keys=True))
    for finding in findings:
        if finding.allowed:
            continue
        level = "WARN" if args.history_warn_only and finding.scope == "git_metadata" else "FAIL"
        print(
            f"{level} {finding.scope} {finding.category} {finding.location}: {finding.redacted()}"
        )
    if unapproved:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
