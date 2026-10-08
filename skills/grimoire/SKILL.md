---
name: grimoire
description: Create, edit, or review Markdown documents for Grimoire, including README, AGENTS.md, and CLAUDE.md files, or answer Grimoire rendering questions. Skip plan-mode plans, auto-memory notes, scratch files, and code-only work.
---

# Writing Markdown for Grimoire

Grimoire is a *confined* Markdown viewer. A document's world is the folder(s) opened in the app, and nothing external or outside those folders loads. Author files so they render and link correctly there.

## Links

- Link between documents with **relative paths** to Markdown files: `[Setup](setup.md)`, `[API](../api/index.md)`. These navigate in-app.
- **Never use absolute paths** (a leading `/`, e.g. `/notes/x.md`). Grimoire flags them as errors and will not resolve them. Everything is relative.
- Keep targets **inside the opened folder tree**. A relative path that escapes it is blocked.
- `http(s)://` links are fine for external references. They open in the real browser (behind a confirmation), not in-app.

## Headings and anchors

- Heading anchors use lowercase text, remove punctuation other than `-` and `_`, and replace spaces with hyphens without collapsing runs.
- **Avoid space-flanked punctuation in headings.** Write "and" instead of ` & `, and avoid spaced slashes or em dashes. Removing that punctuation leaves a double hyphen in the slug (`## A & B` → `#a--b`), which is easy to mis-link.
- Prefer **ASCII headings**. Grimoire strips accented and non-Latin characters from slugs (`## Café` → `#caf`), making those anchors unpredictable.
- A `#anchor` you link to must match the generated slug **exactly**. Grimoire does not warn on a wrong anchor; the link just won't jump.

## Images

- Reference images by **relative path within the opened folder**: `![diagram](assets/diagram.png)`. Supported: PNG, JPEG, GIF, WebP, SVG, BMP, ICO, AVIF.
- **No external image URLs**, and no images outside the opened folders. Both are blocked and show a placeholder.

## Callouts
A blockquote whose **first line** is `[!TYPE]` renders as a colored callout box (GitHub-style), not a plain quote. Five case-insensitive types: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.

- The marker must be the callout's **first line** (e.g. `> [!WARNING]`, then the body on the following `>` lines). The body is normal Markdown, so lists, `inline code`, links, and multiple paragraphs all nest inside.
- A plain blockquote with **no** `[!TYPE]` marker stays an ordinary quote. Callouts are opt-in.

## Front matter
A YAML block fenced by `---` at the **very top** of the file (nothing above it) renders as a small metadata table instead of leaking into the page as stray text.

- Supported shapes: scalars, quoted strings, `[a, b]` inline arrays, `- item` lists, and **one** level of nesting. Anything more exotic falls back to showing the raw block, so keep the front matter simple.
- It only counts as front matter when it's the **first thing** in the file. A `---` block anywhere else is ordinary Markdown (a horizontal rule).

## Math (LaTeX)
Write math with `$…$` inline and `$$…$$` for a display block, rendered by KaTeX (local, offline). Grimoire does not recognize `\[ … \]` or `\( … \)` as math delimiters. KaTeX covers standard **math-mode** LaTeX (sub/superscripts, `\frac`, `\sqrt`, Greek, `\mathbf`, the `array` environment, etc.) but **not** full-document LaTeX.

- For multi-line math, use `aligned` or `gathered` inside `$$`.
- Avoid `multline`, `\label`, `\ref`, `\eqref`, `\usepackage`, TikZ, and other full-LaTeX diagram packages.
- [KaTeX supports](https://katex.org/docs/supported.html) `equation`, `align`, and `gather` in display mode, plus `\newcommand` and `\def`. These remain untested in Grimoire. Do not infer app support from library support, or rely on macro definitions carrying between expressions.

## GitHub-style Markdown works
Tables, task lists (`- [ ]`), footnotes, `:emoji:`, and fenced code with a **language tag** for highlighting (```` ```python ````).

## Everything else

### Don't embed external resources via raw HTML
Confinement blocks external `<img>`, `<iframe>`, `<script>`, and remote CSS or fonts. Inline `data:` images are fine.

### Bold/italic around inline math
Never wrap Markdown emphasis (`**bold**` or `*italic*`) around a span that contains inline math (`$...$`). When emphasis delimiters straddle a math token, the renderer fails to pair them and the literal `**` or `*` leaks into the output as visible stars.

- Bad:  `**Where $k=0,\dots,11$ comes from.**`
- Good: `**Where the range comes from.**` then the sentence with `$k=0,\dots,11$` left unbolded.

If a heading or phrase needs both emphasis and math, split them so no emphasis run crosses a `$...$` boundary. Emphasis with no math inside it is fine.
