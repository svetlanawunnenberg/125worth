# 125 Worth Avenue, Palm Beach

Project base for the 125 Worth Avenue renovation (Fairfax & Sammons Architects for L3 Capital).

**Start with [`text/00_INDEX.md`](text/00_INDEX.md)**: project facts, people, timeline and the list of documents.

## How it works
- `sources/` holds every file exactly as received, in dated folders.
- `pages/` holds slide and page images for quick viewing.
- `text/` holds searchable write-ups of each source, including descriptions of the drawings and images.

The `text/` files are also saved to the "125 Worth Ave" Project on claude.ai, so you can ask questions about anything in them from any chat in that Project.

## Adding new material
Upload the file to a chat in the "125 Worth Ave" Project and say "add this to the 125 base."

## Search site
`index.html` is a public search page for everything in `text/`, served by GitHub Pages at
https://svetlanawunnenberg.github.io/125worth/

After adding or editing anything in `text/`, rebuild the search data with:

    python3 scripts/build_search.py

To show a picture with a passage, add a Markdown image line such as
`![Spec sheet](../pages/lanterns/Example.jpg)` inside that section.
