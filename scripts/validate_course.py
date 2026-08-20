#!/usr/bin/env python3
"""Validate the public workshop repository without third-party packages."""

from __future__ import annotations

import html
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "index.html"
LAB = ROOT / "assets" / "agentic-analytics-lab"
LAB_ZIP = ROOT / "assets" / "agentic-analytics-workshop-lab.zip"
PROMPTS = ROOT / "prompts"


class CourseParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag in {"a", "link", "script", "img"}:
            target = values.get("href") or values.get("src")
            if target:
                self.links.append(target)


def normalize(value: str) -> str:
    return " ".join(value.replace("\r\n", "\n").split())


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_html(errors: list[str]) -> None:
    source = COURSE.read_text(encoding="utf-8")
    html_files = [COURSE, *sorted((ROOT / "examples").rglob("*.html"))]
    for html_file in html_files:
        parser = CourseParser()
        parser.feed(html_file.read_text(encoding="utf-8"))

        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicates:
            fail(
                errors,
                f"duplicate HTML ids in {html_file.relative_to(ROOT)}: {', '.join(duplicates)}",
            )

        for target in parser.links:
            parsed = urlsplit(target)
            if target.startswith("#"):
                fragment = unquote(parsed.fragment)
                if fragment and fragment not in parser.ids:
                    fail(
                        errors,
                        f"missing internal anchor in {html_file.relative_to(ROOT)}: {target}",
                    )
                continue
            if parsed.scheme in {"http", "https", "mailto", "data"}:
                continue
            path = unquote(parsed.path)
            if path and not (html_file.parent / path).exists():
                fail(
                    errors,
                    f"missing relative link in {html_file.relative_to(ROOT)}: {target}",
                )

    page_text = normalize(html.unescape(source))
    prompt_files = sorted(PROMPTS.glob("[0-9]*.md"))
    if len(prompt_files) != 8:
        fail(errors, f"expected 8 standalone prompts, found {len(prompt_files)}")
    for prompt_file in prompt_files:
        text = prompt_file.read_text(encoding="utf-8")
        match = re.search(r"```text\n(.*?)\n```", text, re.DOTALL)
        if not match:
            fail(errors, f"missing text prompt block: {prompt_file.relative_to(ROOT)}")
            continue
        if normalize(match.group(1)) not in page_text:
            fail(errors, f"standalone prompt is out of sync with index.html: {prompt_file.name}")


def check_zip(errors: list[str]) -> None:
    disk_files = {
        path.relative_to(LAB).as_posix(): path.read_bytes()
        for path in LAB.rglob("*")
        if path.is_file()
    }
    with zipfile.ZipFile(LAB_ZIP) as archive:
        zip_files = {
            name: archive.read(name)
            for name in archive.namelist()
            if not name.endswith("/")
        }
    if disk_files.keys() != zip_files.keys():
        missing = sorted(disk_files.keys() - zip_files.keys())
        extra = sorted(zip_files.keys() - disk_files.keys())
        fail(errors, f"lab ZIP paths differ; missing={missing}, extra={extra}")
        return
    changed = sorted(name for name in disk_files if disk_files[name] != zip_files[name])
    if changed:
        fail(errors, f"lab ZIP content differs: {', '.join(changed)}")


def check_public_boundary(errors: list[str]) -> None:
    markers = (
        "/Users/",
        "Paras-OS",
        "interview-os",
        "contact@parasdoshi.com",
        "rinuandparas@gmail.com",
        "Opendoor",
        "BlackLine",
        "PadSplit",
    )
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path == Path(__file__)
            or ".git" in path.parts
            or path.suffix in {".zip", ".png"}
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in markers:
            if marker in text:
                fail(errors, f"private marker {marker!r} found in {path.relative_to(ROOT)}")


def check_course_content(errors: list[str]) -> None:
    required_sources = (
        "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
        "https://openai.com/index/inside-our-in-house-data-agent/",
        "https://www.anthropic.com/engineering/building-effective-agents",
        "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
        "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
        "https://ai.meta.com/blog/practical-ai-agent-security/",
        "https://github.com/meta-llama/PurpleLlama",
        "https://engineering.ramp.com/post/meet-ramp-research",
        "https://builders.ramp.com/post/how-to-build-agents-users-can-trust",
    )
    course_text = COURSE.read_text(encoding="utf-8")
    for source in required_sources:
        if source not in course_text:
            fail(errors, f"missing leading-practice source in index.html: {source}")

def main() -> int:
    errors: list[str] = []
    check_html(errors)
    check_zip(errors)
    check_public_boundary(errors)
    check_course_content(errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: course and example links, ids, prompts, lab ZIP, and public boundary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
