"""Rasterize the final PDF and record page geometry for visual review."""
from pathlib import Path
import json
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]


def main():
    doc = pymupdf.open(ROOT / 'paper_output/qa/rendered/final_paper.pdf')
    output = ROOT / 'paper_output/qa/rendered/pages'
    output.mkdir(parents=True, exist_ok=True)
    findings = []
    thumbnails = []
    for number, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
        pix.save(output / f'page-{number:03}.png')
        thumb = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        thumb.thumbnail((295, 420))
        tile = Image.new('RGB', (315, 450), 'white')
        tile.paste(thumb, ((315-thumb.width)//2, 20))
        ImageDraw.Draw(tile).text((8, 4), f'Page {number}', fill='black')
        thumbnails.append(tile)
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    box = pymupdf.Rect(span['bbox'])
                    if box.x0 < -1 or box.y0 < -1 or box.x1 > page.rect.width+1 or box.y1 > page.rect.height+1:
                        findings.append({'page': number, 'kind': 'out_of_page', 'text': span['text'][:80], 'bbox': list(box)})
    for start in range(0, len(thumbnails), 12):
        sheet = Image.new('RGB', (1260, 1350), '#cbd0d6')
        for offset, tile in enumerate(thumbnails[start:start+12]):
            sheet.paste(tile, ((offset%4)*315, (offset//4)*450))
        sheet.save(output / f'contact-{start//12+1:02}.png')
    print(json.dumps({'pages':len(doc),'geometry_findings': findings}, ensure_ascii=False))


if __name__ == '__main__':
    main()
