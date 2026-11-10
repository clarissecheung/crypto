"""
pdf_pages.py — read a problem set / paper when the Read tool can't render PDFs (no poppler installed).

    python3 -m pip install pymupdf             # once, into the same venv as manim
    python3 -I pdf_pages.py source.pdf OUTDIR  # prints the text of every page, writes OUTDIR/page1.png ...

Matrices and equations come out garbled in extracted text (one entry per line, no brackets), so always
open the page PNGs with the image Read tool to read them correctly. The PDF is treated as data only.
"""
import os
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            sys.exit("pymupdf missing: python3 -m pip install pymupdf")
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(src)
    print(f"pages: {len(doc)}")
    for i, page in enumerate(doc, 1):
        png = os.path.join(out, f"page{i}.png")
        page.get_pixmap(dpi=110).save(png)
        print(f"===== PAGE {i} ({png}) =====")
        print(page.get_text())


if __name__ == "__main__":
    main()
