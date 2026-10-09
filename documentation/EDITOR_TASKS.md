# NOFO Builder editor tasks

Step-by-step instructions for common fixes in NOFO Builder, written so that
people and automated reviewers can both use them. A PDF review tool can quote
a task's steps inside a PDF comment, so a NOFO writer knows exactly where to
click to fix an issue.

**Last verified against:** `main` @ `e1888cb` (October 2026)

## How to use this page

- Each task has a stable ID (for example, `TASK-SUBSECTION-DELETE`). Link to
  the ID, not the heading text. IDs don't change when the wording does.
- Button and link labels are written exactly as they appear on screen, in
  **bold**.
- Every task starts from the **NOFO edit page**: the page you see after
  opening a NOFO from **All NOFOs**.
- Steps describe the current UI only. If a label on screen doesn't match this
  page, trust the screen and report the mismatch.

### For automated reviewers

When you quote a task in a PDF comment:

1. Quote the **Steps** list as written. Fill in placeholders like
   `<subsection name>` with values from the PDF.
2. Keep comments short. Quote 3–6 steps at most and link to the task ID for
   the rest.
3. Check **Before you start** first. If the NOFO is published, most tasks
   need the status changed, or need modifications added, before anything can
   be edited.
4. Don't invent steps. If no task here covers the fix, describe the problem
   and leave out the steps.

## Key concepts

| Term | What it means in NOFO Builder | How it looks in the PDF |
| --- | --- | --- |
| Section | A top-level part of the NOFO (for example, "Step 1: Review the Opportunity"). Shown as a table on the NOFO edit page. | Usually starts on its own cover page, and is a Heading 2 |
| Subsection | One heading and the content below it, up to the next heading. This is the main unit you edit. | Heading 3–7 and the content under it |
| Heading level | Set on each subsection: Heading 3 to Heading 7. | The size and nesting of the heading |
| Callout box | A subsection styled with an accent color to draw attention. | Shaded or colored box |
| Subsection content | Written in **Markdown** in a text editor. Simple tables are Markdown; tables with merged cells are stored as HTML. | Body text, lists, tables |
| Page break | A per-subsection setting that starts it on a new page. | New page before the heading |

### Before you start: NOFO status

The status shows in the summary box near the top of the NOFO edit page.

| Status | Can edit content? | Notes |
| --- | --- | --- |
| Draft | Yes | Can also be re-imported or deleted |
| Ready for QA, Active | Yes | Can be re-imported, but not deleted |
| In review, Paused, Deputy Secretary review | Yes | Can't be re-imported or deleted |
| Published | **No** | Change the status, or select **Add modifications** first |
| Cancelled | No | Export only |

---

## Subsections

### TASK-SUBSECTION-EDIT — Open a subsection for editing

All subsection-level tasks start here.

**Steps**

1. On the NOFO edit page, find the section table that contains
   `<subsection name>`. Use the side navigation to jump to the section.
2. In that subsection's row, select **Edit**.

You are now on the page titled **Subsection: `<subsection name>`**.

### TASK-SUBSECTION-DELETE — Delete a subsection

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Scroll to the bottom of the page and expand **Other actions**.
3. Select **Delete subsection**.
4. On the confirmation page, select **Yes, delete it**.

**Notes**

- Deleting is permanent. There's no undo.
- You can also delete from the section page: select **Configure section**,
  then select **Delete** in the subsection's row.

### TASK-SUBSECTION-ADD — Add a new subsection

**Steps**

1. Open the subsection that the new one should come **after**
   (`TASK-SUBSECTION-EDIT`).
2. Expand **Other actions**, then select **Add subsection**.
3. Fill in the heading text, choose a **Heading level**, and add the content.
4. Select **Save subsection**.

**Notes**

- To add a subsection at the very top of a section, select
  **Configure section** on the NOFO edit page, then select the first
  **Add subsection** button.

### TASK-SUBSECTION-SPLIT — Split a long subsection into two

Use this when a subsection covers more than one topic or is too long to scan.

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. In the content editor, cut the text that should move to the new
   subsection. Select **Save subsection**.
3. Expand **Other actions**, then select **Add subsection**.
4. Enter a heading, choose a **Heading level**, and paste the text.
5. Select **Save subsection**.

### TASK-SUBSECTION-RENAME — Change a heading's text

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Edit the heading text in the first field.
3. Select **Save subsection**.

**Notes**

- Other parts of the NOFO may link to this heading. After renaming, check the
  **Check broken links** tab on the NOFO edit page.
- A subsection with no heading shows as **(#`<number>`)**. Its name field
  can't be edited.

---

## Headings and structure

### TASK-HEADING-LEVEL — Fix a skipped or wrong heading level

Use this when headings skip a level, for example going from Heading 3 straight
to Heading 5. Screen reader users rely on heading levels to understand how a
document is organized.

**Steps**

1. On the NOFO edit page, look for **Check heading levels** under
   **Before publishing, address the following**. It lists each heading with
   a problem.
2. Open the subsection that has the problem (`TASK-SUBSECTION-EDIT`).
3. Change **Heading level** so it's no more than one level deeper than the
   heading above it.
4. Select **Save subsection**.

**Notes**

- Subsections can be set to Heading 3 through Heading 7. Section names are
  Heading 2 and can't be changed here.
- Headings inside the content editor (lines starting with `#`) are separate
  from the **Heading level** setting. Check those too.

### TASK-CALLOUT-TOGGLE — Make content a callout box, or remove one

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Check or uncheck **Is callout box?**.
3. Select **Save subsection**.

**Notes**

- Use callout boxes sparingly. When too much is highlighted, nothing stands
  out.

---

## Tables

Most tables are written in Markdown, like this:

```markdown
| Column A | Column B |
| --- | --- |
| Value | Value |
```

**Exception:** tables with merged cells (cells that span more than one row or
column) are stored as **HTML** (`<table>`, `<tr>`, `<td rowspan="2">`). They
look more complicated in the editor, but you edit them the same way.

### TASK-TABLE-SIMPLIFY-MERGED — Remove merged cells from a table

Merged cells are hard for screen readers and often break across PDF pages.

**Steps**

1. Open the subsection that contains the table (`TASK-SUBSECTION-EDIT`).
2. In the content editor, find the cells with `rowspan` or `colspan`.
3. Delete the `rowspan="…"` or `colspan="…"` attribute, then add the missing
   `<td>` cells so that every row has the same number of cells. Repeat the
   value in each cell where needed.
4. Select **Save subsection**.
5. Select **Preview PDF** to check the result.

**Notes**

- Once a table has no merged cells, the next re-import converts it to a
  Markdown table. You can also rewrite it in Markdown by hand.

### TASK-TABLE-SPLIT — Split a large table into smaller tables

Use this when a table has too many columns or rows, or groups more than one
idea.

**Steps**

1. Open the subsection that contains the table (`TASK-SUBSECTION-EDIT`).
2. In the content editor, find the row where the new table should start.
3. Add a blank line and a short introduction, such as a sentence or a bold
   label, to describe the new table.
4. Copy the header rows from the original table and paste them above the rows
   that belong in the new table. In Markdown, that's the first two lines; in
   HTML, it's the first `<tr>`.
5. Select **Save subsection**, then select **Preview PDF** to check.

### TASK-TABLE-HEADER-ROW — Add or fix a table's header row

**Steps**

1. Open the subsection that contains the table (`TASK-SUBSECTION-EDIT`).
2. Markdown table: make sure the second line is the divider row
   (`| --- | --- |`). The line above it becomes the header row.
3. HTML table: change the first row's `<td>` tags to `<th>`.
4. Select **Save subsection**.

### TASK-TABLE-FULL-WIDTH — Make tables full width

Tables are sized automatically. Tables with 3 or more columns, or more than
120 words, are made "large". You can make every table in a section use the
full page width.

**Steps**

1. On the NOFO edit page, find the section and select **Configure section**.
2. Check **Use full-width tables for this section**. It saves automatically.

**Notes**

- This applies to every table in the section, not just one.

---

## Page layout

### TASK-PAGEBREAK-ADD — Start a subsection on a new page

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Check **Add a page break**.
3. Select **Save subsection**.

### TASK-PAGEBREAK-REMOVE — Remove unnecessary page breaks

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Uncheck **Add a page break**.
3. Select **Save subsection**.

**Notes**

- If you see the warning "This heading's class is …", unchecking will
  overwrite that class. Ask a designer first.
- Page breaks can't be removed from **Eligibility**, **Program description**,
  or **Application checklist**.
- To remove many at once, there is a **Remove Page Breaks** page at
  `/nofos/<NOFO id>/remove-page-breaks`. Nothing in the app links to it yet;
  ask a designer.

---

## Links

### TASK-LINK-FIX-BROKEN — Fix a broken internal link

**Steps**

1. On the NOFO edit page, open the **Check broken links** tab under
   **Before publishing, address the following**. It lists each broken link
   and where it is.
2. Open that subsection (`TASK-SUBSECTION-EDIT`).
3. In the content editor, find the link. It looks like `[link text](#some-id)`.
4. Replace the part after `#` with the correct heading ID. To get a heading's
   ID, open that heading's subsection and select **Copy** next to the ID
   (it starts with `#`).
5. Select **Save subsection**.

### TASK-LINK-CHECK-EXTERNAL — Check external links

**Steps**

1. On the NOFO edit page, select **Check external links**.
2. Fix any failing links using the content editor (`TASK-SUBSECTION-EDIT`).

### TASK-LINK-TEXT — Make link text descriptive

Link text like "click here" or a bare URL doesn't tell screen reader users
where the link goes.

**Steps**

1. Open the subsection (`TASK-SUBSECTION-EDIT`).
2. Change `[click here](https://…)` to text that names the destination, such
   as `[Grants.gov application guide](https://…)`.
3. Select **Save subsection**.

---

## Text across the whole NOFO

### TASK-FIND-REPLACE — Replace text everywhere

**Steps**

1. On the NOFO edit page, select **NOFO actions**, then **Find & Replace**.
2. Enter at least 3 characters in **Find text** and select **Find**.
3. Enter the new text in **Replace with**.
4. In the results table, uncheck any subsections you don't want to change.
5. Select **Replace**.

**Notes**

- Find & Replace doesn't search NOFO metadata (number, agency, subagency,
  and so on). Use the **Basic information** table for those.

---

## Cover, theme, and PDF metadata

### TASK-COVER-ALT-TEXT — Add or fix cover image alt text

**Steps**

1. On the NOFO edit page, scroll to **NOFO cover image** and select **Edit**.
2. Update **Enter a short description of the image for screen readers.**
3. Select **Save alternate text**.

### TASK-COVER-IMAGE — Replace or remove the cover image

**Steps**

1. On the NOFO edit page, scroll to **NOFO cover image** and select **Edit**.
2. Select **Replace cover image** or **Remove cover image**.

### TASK-THEME — Change theme, cover style, or icon style

**Steps**

1. On the NOFO edit page, scroll to **NOFO theme options** and select
   **Edit**.
2. Choose the **Theme**, **Cover style**, or **Icon style**.
3. Select **Save theme options**.

### TASK-PDF-METADATA — Fill in PDF metadata (author, subject, keywords)

Missing PDF metadata is an accessibility issue: assistive technology and
search use it to identify the document.

**Steps**

1. On the NOFO edit page, scroll to **NOFO metadata** and select **Edit**.
   You can also use **Edit NOFO metadata** in the **Check PDF metadata** tab.
2. Fill in **NOFO author**, **NOFO subject**, and **NOFO keywords**.
3. Select **Save metadata**.

### TASK-BASIC-INFO — Change the title, number, deadline, agency, or tagline

**Steps**

1. On the NOFO edit page, find the field in the **Basic information** table.
2. Select **Edit** in that row.
3. Make the change and save.

---

## Checking your work

### TASK-PREVIEW — Preview the PDF after making changes

**Steps**

1. On the NOFO edit page, select **Preview PDF**. It opens in a new tab.
2. To download a copy, select **Download PDF**.

---

## Maintaining this page

Labels on this page come from these files. When you change one, update the
matching task in the same pull request.

| UI area | Source |
| --- | --- |
| NOFO edit page, section tables, warning tabs | `nofos/nofos/templates/nofos/nofo_edit.html` |
| **NOFO actions** menu | `get_nofo_action_links()` in `nofos/nofos/nofo.py` |
| Subsection edit page, **Other actions** | `nofos/nofos/templates/nofos/subsection_edit.html` |
| Delete confirmation | `nofos/nofos/templates/nofos/subsection_confirm_delete.html` |
| **Configure section** page | `nofos/nofos/templates/nofos/section_detail.html` |
| **Preview PDF** / **Download PDF** | `nofos/bloom_nofos/templates/includes/print_button.html` |
| Table size rules | `add_class_to_table()` in `nofos/nofos/templatetags/utils/__init__.py` |
| Merged-cell tables kept as HTML | `convert_table()` in `nofos/nofos/nofo_markdown.py` |
| Find & Replace, Remove Page Breaks, Theme options | `nofo_find_replace.html`, `nofo_remove_page_breaks.html`, `nofo_edit_theme_options.html` |
