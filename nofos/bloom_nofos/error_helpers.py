from dataclasses import dataclass

from bloom_nofos.import_errors import (
    DOCUMENT_STRUCTURE_RECOVERY_STEPS,
    IMPORT_ERROR_CATALOG,
)
from django.core.exceptions import ValidationError
from django.shortcuts import render

__all__ = [
    "DOCUMENT_STRUCTURE_RECOVERY_STEPS",
    "AmbiguousHeadingHierarchyError",
    "LongHeading",
    "MistaggedHeadingError",
    "StrictFormattingError",
    "render_blocking_import_error",
    "render_import_error",
    "render_import_server_error",
    "render_mistagged_heading_error",
]


# Word's Find box accepts at most 255 characters, so the error page offers a
# short phrase to search for instead of the whole heading.
SEARCH_SNIPPET_LENGTH = 60

# Characters of each heading to include in the warning log: enough to
# recognize it, without copying whole paragraphs of NOFO text into the logs.
LOG_TEXT_PREVIEW_LENGTH = 100

# Longest section name to repeat when saying where a subsection sits.
LOCATION_SECTION_NAME_LENGTH = 80


def _truncate(text, length):
    return text if len(text) <= length else text[: length - 1].rstrip() + "…"


@dataclass
class LongHeading:
    """One heading whose text is over its character limit."""

    kind: str  # "section" or "subsection"
    order: int | str | None
    text: str
    max_length: int
    # The tag the heading came from ("h1".."h6", or "div" for Heading 7),
    # when the parser recorded it. Used to name the Word style.
    source_tag: str = ""
    # Text before the heading's first line break (Shift+Enter), when it has
    # one. Empty when the heading is a single line.
    first_line: str = ""
    # For a subsection, the name of the section it sits under.
    section_name: str = ""

    @property
    def length(self):
        return len(self.text)

    @property
    def has_line_break(self):
        return bool(self.first_line)

    @property
    def word_style(self):
        tag = (self.source_tag or "").lower()
        if tag in ("div", "h7"):
            return "Heading 7"
        if len(tag) == 2 and tag[0] == "h" and tag[1].isdigit():
            return f"Heading {tag[1]}"
        return ""

    @property
    def search_snippet(self):
        """
        The start of the heading, cut at a word boundary, to paste into Word's
        Find box. Taken from the first line when the heading has a line break,
        because the extracted text runs the lines together and would not match.
        """
        text = " ".join((self.first_line or self.text).split())
        if len(text) <= SEARCH_SNIPPET_LENGTH:
            return text
        snippet = text[:SEARCH_SNIPPET_LENGTH]
        last_space = snippet.rfind(" ")
        if last_space > SEARCH_SNIPPET_LENGTH // 2:
            snippet = snippet[:last_space]
        return snippet

    @property
    def location(self):
        if self.kind == "section":
            if self.order not in (None, ""):
                return f"Main section heading (section {self.order})"
            return "Main section heading"
        if self.section_name:
            section_name = _truncate(self.section_name, LOCATION_SECTION_NAME_LENGTH)
            return f"Under the section “{section_name}”"
        return "Subsection heading"

    def log_details(self):
        return {
            "kind": self.kind,
            "order": self.order,
            "word_style": self.word_style,
            "section_name": _truncate(self.section_name, LOG_TEXT_PREVIEW_LENGTH),
            "length": self.length,
            "max_length": self.max_length,
            "has_line_break": self.has_line_break,
            "text_preview": self.text[:LOG_TEXT_PREVIEW_LENGTH],
        }


class MistaggedHeadingError(ValidationError):
    """
    One or more headings are too long, which almost always means paragraph
    text carrying a heading style. Carries every such heading so the user can
    fix them all before importing again, not one per attempt.
    """

    code = "mistagged_heading"

    def __init__(self, headings):
        self.headings = list(headings)
        first = self.headings[0]
        message = (
            f"{first.kind.title()} heading {first.order} exceeds the "
            f"{first.max_length}-character limit. This often means a paragraph "
            "was incorrectly styled as a heading."
        )
        if len(self.headings) > 1:
            message += (
                f" {len(self.headings) - 1} more heading(s) also exceed their limit."
            )
        super().__init__(message, code=self.code)

    def log_details(self):
        """Structured fields for log_exception(), so support can triage from logs."""
        return {
            "long_heading_count": len(self.headings),
            "long_headings": [heading.log_details() for heading in self.headings],
        }


class StrictFormattingError(ValidationError):
    """
    Strict import mode found Word styles that aren't in our style map.

    Carries the style warnings as data so the error page can list them as
    details, rather than folding them into the message string.
    """

    code = "strict_formatting"

    def __init__(self, warnings):
        self.warnings = list(warnings)
        super().__init__(
            "These styles are not recognized by our style map: {}".format(
                "; ".join(self.warnings)
            ),
            code=self.code,
        )


class AmbiguousHeadingHierarchyError(ValidationError):
    """
    A Heading 2 appears before the document's first Heading 1, so the level
    that marks a main section can't be determined without silently dropping
    content. Carries both headings so the error page can show them.
    """

    code = "ambiguous_heading_hierarchy"

    def __init__(self, *, h2_text, h1_text, preceding_h2_count=None):
        self.h2_text = h2_text
        self.h1_text = h1_text
        self.preceding_h2_count = preceding_h2_count
        super().__init__(
            (
                "The document uses Heading 2 before its first Heading 1. "
                f'NOFO Builder would skip content beginning with Heading 2 "{h2_text}" '
                f'and start at Heading 1 "{h1_text}".'
            ),
            code=self.code,
        )


def render_blocking_import_error(
    request,
    *,
    title,
    summary,
    error_code,
    status=400,
    recovery_steps=None,
    retry_url=None,
    retry_label="Try the import again",
    error_details=None,
    error_detail_groups=None,
):
    """Render a safe, actionable error page for a blocked document import."""
    return render(
        request,
        "import_error.html",
        status=status,
        context={
            "error_title": title,
            "error_summary": summary,
            "error_code": error_code,
            "recovery_steps": recovery_steps or [],
            "retry_url": retry_url,
            "retry_label": retry_label,
            "error_details": error_details or [],
            "error_detail_groups": error_detail_groups or [],
        },
    )


def render_import_error(
    request,
    error_code,
    *,
    retry_url=None,
    retry_label="Try the import again",
    error_details=None,
    error_detail_groups=None,
    summary_context=None,
):
    """
    Render the error page for a catalogued import error code.

    Copy comes from IMPORT_ERROR_CATALOG so there is one place to read and
    change it. `error_details` carries the per-failure specifics (the offending
    heading, the unrecognized styles); `summary_context` fills placeholders in
    the catalog's summary, for the rare entry that needs one.
    """
    entry = IMPORT_ERROR_CATALOG[error_code]
    summary = entry["summary"]
    if summary_context:
        summary = summary.format(**summary_context)

    return render_blocking_import_error(
        request,
        title=entry["title"],
        summary=summary,
        error_code=error_code,
        status=entry["status"],
        recovery_steps=list(entry["recovery_steps"]),
        retry_url=retry_url,
        retry_label=retry_label,
        error_details=error_details,
        error_detail_groups=error_detail_groups,
    )


def render_mistagged_heading_error(
    request,
    error,
    *,
    retry_url=None,
    retry_label="Try the import again",
):
    """
    Render one page listing every heading that is over its character limit,
    with enough detail to find each one in Word.
    """
    count = len(error.headings)
    groups = []
    for number, heading in enumerate(error.headings, start=1):
        details = [{"label": "Where", "value": heading.location}]
        if heading.word_style:
            details.append({"label": "Word style", "value": heading.word_style})
        details.append(
            {
                "label": "Length",
                "value": (
                    f"{heading.length} characters "
                    f"(the limit is {heading.max_length})"
                ),
            }
        )
        if heading.has_line_break:
            details.append(
                {
                    "label": "Likely cause",
                    "value": (
                        "A line break (Shift+Enter) joins this heading to the "
                        "text after it, so Word treats them as one heading."
                    ),
                }
            )
        details.append(
            {
                "label": "Search Word for",
                "value": heading.search_snippet,
                "is_code": True,
            }
        )
        groups.append(
            {
                "title": (
                    f"Heading {number} of {count}" if count > 1 else "Heading text"
                ),
                "details": details,
                "full_text": heading.text,
            }
        )

    return render_import_error(
        request,
        "IMPORT-HEADING-TOO-LONG",
        error_details=[
            {"label": "Headings over the limit", "value": str(count)},
        ],
        error_detail_groups=groups,
        retry_url=retry_url,
        retry_label=retry_label,
    )


def render_import_server_error(request, *, retry_url=None):
    """Return a sanitized 500 response for an unexpected import failure."""
    return render_import_error(
        request,
        "IMPORT-UNEXPECTED",
        retry_url=retry_url,
    )
