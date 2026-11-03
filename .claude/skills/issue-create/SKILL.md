---
name: issue-create
description: Draft a GitHub issue for HHS/simpler-grants-pdf-builder that follows the repository's issue templates, label conventions and triage guidance. Use when asked to file, write, draft or open a bug report, feature request or documentation issue for NOFO Builder.
---

# Create an issue

Drafts an issue for `HHS/simpler-grants-pdf-builder`. The rules live in the
documents linked below; this skill is the order to apply them in. If a step here
disagrees with a linked document, the document wins: follow it and fix this file.

Read the templates and guides from upstream `main`. A fork or an old branch may
have outdated copies, or none at all.

## 1. Choose the template

| The issue is | Template | Default label |
| --- | --- | --- |
| Something that isn't working | `.github/ISSUE_TEMPLATE/bug_report.md` | `Bug 🐛` |
| A new feature or improvement | `.github/ISSUE_TEMPLATE/feature_request.md` | `Feature request` |
| A documentation change | `.github/ISSUE_TEMPLATE/feature_request.md` | `documentation`, replacing the template's default |

Keep the template's headings and their order. Remove the HTML comments once a
section is filled in.

## 2. Gather the finding

Fill the template with the information in
`documentation/QUALITY_REVIEW_AND_TRIAGE.md` § Record an actionable finding
(`#review-finding`): goal and coverage, observation and evidence, assessment,
recommendation and verification. Use headings in the template where they fit;
put the rest under the closest heading as text.

- Use what the user already gave you (description, screenshots, logs) before
  asking questions. Ask only for what's missing and needed, such as reproduction
  steps, page or URL, date and time, OpDiv, or an error code.
- Follow § Guidance for assisted or automated reviews (`#review-assisted`):
  separate the observation from a suspected cause, say how each piece of
  evidence was obtained, and mark checks you didn't perform as **not checked**.
- For a feature request, describe the unmet need rather than only one
  implementation.

## 3. Propose labels and priority

- Check the repository's live label list and use exact names, including
  capitalization and emoji. Never create a label or a synonym. See
  `documentation/CONTRIBUTION_WORKFLOW.md` § Issue labels (`#issue-labels`).
- Propose a `Priority: high`, `Priority: medium` or `Priority: low` label with a
  one-line rationale based on § Assess impact and priority (`#review-priority`)
  in the triage guide. Record confidence separately (reproduced, observed but not
  reproduced, or reported but not checked). The person doing triage confirms it.

## 4. Check for duplicates

Search open and closed issues for the same problem or request. If one matches,
show it to the user instead of drafting a new issue. If one is related, link it
in the draft.

## 5. Check it's safe to publish

The repository is public. Remove credentials, tokens, cookie values, personal
details and restricted NOFO content. A filename, screenshot or NOFO link can
itself disclose restricted information; if evidence isn't cleared for a public
repository, say so and leave it out.

## 6. Get approval, then post or hand over

Show the user the title, body and labels, and revise until they approve it.
Creating an issue is a separate action from drafting one: don't post an
unapproved draft.

Once the user approves:

- **If you can create issues in `HHS/simpler-grants-pdf-builder`** (through a
  GitHub integration or an authenticated `gh`), create it with the approved
  title, body and labels, then reply with the issue link. Try to create it
  rather than guessing at access in advance. If creation fails because of
  permissions, authentication or a missing tool, say so and hand over instead.
- **Otherwise, hand over** so the user can create it in a few clicks:
  1. A pre-filled link:
     `https://github.com/HHS/simpler-grants-pdf-builder/issues/new?template=<template file>&title=<title>&labels=<labels>&body=<body>`,
     with each value URL-encoded. GitHub applies `labels` only for people who can
     triage the repository; anyone else adds them after creating the issue. If the
     link would be longer than about 8,000 characters, leave out `body`.
  2. The title in one code block and the body in another, as raw Markdown, so
     each copies with one click. Fence the body with four backticks if it
     contains a code block.
  3. The labels to apply, as a list.

The rest of the contribution workflow (branch, PR, CI, squash merge) is in
`documentation/CONTRIBUTION_WORKFLOW.md`.
