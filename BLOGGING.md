# Blogging Playbook

From Obsidian draft to live post in 5 steps.

**Site**: https://arvimal.github.io  
**Theme**: [Congo v2](https://jpanther.github.io/congo/)  
**Deploy**: push to `main` → GitHub Actions builds and deploys (~60s)

---

## Step 1 — Write in Obsidian

Open the SRE Notes vault and create a new note (`Ctrl/Cmd+N`).  
Insert the blog template: `Ctrl/Cmd+P` → *Templates: Insert template* → **Blog Post**.

Fill in the sections:

| Section | Purpose |
|---|---|
| **What** | One paragraph — what is this and why does it matter? |
| **How it works** | Core concepts, internals, mechanics |
| **Practical example** | A concrete command sequence or working snippet |
| **Key takeaways** | 3–5 bullet summary |
| **References** | Links to source material |

Leave `draft: true` and the YAML front matter as-is — you'll set those in Hugo.  
Write freely. The Obsidian note is your scratch pad; polish happens in step 3.

---

## Step 2 — Scaffold the Hugo post

In any terminal:

```bash
newpost "Your Post Title Here"
```

This creates `content/posts/YYYY/your-post-title-here.md` inside the blog repo with pre-filled front matter.

The file opens ready to edit. Confirm the path printed matches the year you intend.

**If the post has images**, convert it to a page bundle instead:

```bash
# Replace the flat file with a bundle directory
SLUG="your-post-title-here"
YEAR=$(date +%Y)
mkdir -p ~/Dropbox/Study/02-Projects/Blog-and-FrontPage/Projects/arvimal.github.io/content/posts/$YEAR/$SLUG
mv ~/Dropbox/Study/02-Projects/Blog-and-FrontPage/Projects/arvimal.github.io/content/posts/$YEAR/${SLUG}.md \
   ~/Dropbox/Study/02-Projects/Blog-and-FrontPage/Projects/arvimal.github.io/content/posts/$YEAR/$SLUG/${SLUG}.md
# Then drop images into the same directory — reference them as ![alt](image.jpg)
```

---

## Step 3 — Copy content and set front matter

Open the Hugo post file and paste your Obsidian content below the front matter.

Set the front matter fields:

```yaml
---
title: "Your Post Title Here"
date: 2026-04-20          # today's date
description: "One sentence that appears in cards and search results."
draft: true               # keep true until ready to publish
tags:
  - linux                 # 2–4 lowercase tags
  - kernel
---
```

**Tag conventions**: use lowercase, hyphen-separated. Check existing tags at  
`content/posts/` for consistency (e.g. `python`, `object-oriented-programming`, `ceph`).

**Code blocks**: use fenced blocks with a language hint — Hugo highlights them:

````markdown
```python
def example():
    pass
```
````

---

## Step 4 — Preview locally

```bash
blog
```

This `cd`s into the blog repo and runs `hugo server -D` (drafts visible).  
Open http://localhost:1313 and check:

- Post appears in the listing
- Code blocks render with syntax highlighting
- No broken images or raw `[code]` tags
- Title and description look right in the card view

`Ctrl+C` to stop the server when done.

---

## Step 5 — Publish

When the post looks right, set `draft: false` in the front matter, then:

```bash
cd $BLOG
git add content/posts/
git commit -m "Add post: Your Post Title Here"
git push
```

GitHub Actions picks up the push, builds with Hugo, and deploys to GitHub Pages.  
Live in ~60 seconds at: `https://arvimal.github.io/posts/YYYY/your-post-title-here/`

---

## Quick reference

| Command | What it does |
|---|---|
| `newpost "Title"` | Scaffold a new post with front matter |
| `blog` | Start local preview server (drafts visible) |
| `cd $BLOG` | Go to blog repo root |
| `git add content/posts/ && git commit -m "..."` | Stage and commit |
| `git push` | Deploy (triggers GitHub Actions) |

---

## Congo theme features worth using

| Feature | How to enable |
|---|---|
| Table of contents | Global — on by default for all posts |
| Series | Add `series: ["Series Name"]` to front matter; links related posts |
| Hero image | Drop a `featured.jpg` in the page bundle directory |
| Math (KaTeX) | Add `math: true` to front matter |
| Diagrams (Mermaid) | Add `mermaid: true` to front matter; use ` ```mermaid ` blocks |

---

## Troubleshooting

**Post doesn't appear in preview**  
→ Check `draft: true` is set and you're running `hugo server -D`.

**Code block shows as raw text**  
→ Ensure the fence uses triple backticks, not `[code language="..."]` (WordPress artifact).

**Push rejected**  
→ Run `git pull --rebase origin main` first, then push again.

**Build fails in GitHub Actions**  
→ Check the Actions tab on GitHub for the error. Most common cause: malformed front matter YAML.
