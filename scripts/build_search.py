"""Build search-data.js for the 125 Worth search site.

Run from the repo root after adding or editing anything in text/:
    python3 scripts/build_search.py

Each text/*.md file becomes a document. Each document is split into
searchable passages at headings and at bold-led paragraphs (one per slide,
one per email, one per fixture). Passages that mention a slide number are
linked to that slide's image in pages/arcom-presentation/.
"""
import json
from datetime import date
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
SLIDES = ROOT / "pages" / "arcom-presentation"


def doc_title(md, fallback):
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else fallback


def passage_images(text):
    """Slide images for "**Slide N" passages, plus any ![](path) images."""
    imgs = []
    m = re.match(r"\*\*Slides?\s+(\d+)(?:\s+(?:to|-)\s+(\d+))?", text)
    if m:
        a = int(m.group(1))
        b = int(m.group(2) or a)
        imgs += [f"pages/arcom-presentation/slide-{n:02d}.jpg" for n in range(a, b + 1)
                 if (SLIDES / f"slide-{n:02d}.jpg").exists()]
    for path in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        path = path.replace("../", "", 1)
        if (ROOT / path).exists():
            imgs.append(path)
    return imgs


def chunks_for(doc_id, md):
    out = []
    heading = ""
    buf = []

    def flush():
        body = "\n".join(buf).strip()
        if body:
            first = body.splitlines()[0]
            m = re.match(r"\*\*(.+?)\*\*", first)
            title = m.group(1).rstrip(".:") if m else heading
            out.append({
                "doc": doc_id,
                "section": heading,
                "title": title or heading,
                "text": body,
                "images": passage_images(body),
            })
        buf.clear()

    for line in md.splitlines():
        if re.match(r"^#{1,3}\s", line):
            flush()
            heading = line.lstrip("#").strip()
            continue
        if line.startswith("**") and (not buf or buf[-1].strip() == ""):
            flush()
        buf.append(line)
    flush()
    return out


def main():
    docs, chunks = [], []
    for path in sorted(TEXT.glob("*.md")):
        md = path.read_text(encoding="utf-8")
        doc_id = path.stem
        docs.append({"id": doc_id, "file": f"text/{path.name}",
                     "title": doc_title(md, doc_id), "md": md})
        chunks.extend(chunks_for(doc_id, md))
    slides = sorted(p.name for p in SLIDES.glob("slide-*.jpg"))
    data = {"updated": date.today().strftime("%B %-d, %Y"), "docs": docs, "chunks": chunks, "slides": slides}
    (ROOT / "search-data.js").write_text(
        "window.SEARCH_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8")
    print(f"{len(docs)} documents, {len(chunks)} passages, {len(slides)} slides")


if __name__ == "__main__":
    main()
