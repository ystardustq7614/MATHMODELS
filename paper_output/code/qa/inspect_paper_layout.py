"""Render contact sheets and check contest-specific physical PDF constraints."""
from pathlib import Path
import json
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'paper_output'


def main():
    pdf = pymupdf.open(OUT/'qa/rendered/final_paper.pdf')
    folder = OUT/'qa/rendered/inspection'
    folder.mkdir(exist_ok=True)
    outside = []
    for i, page in enumerate(pdf):
        for word in page.get_text('words'):
            if word[0] < 65 or word[2] > page.rect.width-65:
                outside.append({'page':i+1,'text':word[4],'bbox':word[:4]})
    for start in range(0,len(pdf),12):
        sheet = Image.new('RGB',(1000,1100),'#dddddd')
        draw = ImageDraw.Draw(sheet)
        for i in range(start,min(start+12,len(pdf))):
            pix=pdf[i].get_pixmap(matrix=pymupdf.Matrix(.38,.38),alpha=False)
            image=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
            image.thumbnail((235,335))
            x=(i-start)%4*250+7
            y=(i-start)//4*365+20
            sheet.paste(image,(x,y))
            draw.text((x,y-15),str(i+1),fill='black')
        sheet.save(folder/f'contact_{start+1:03d}.png')
    for i in [0,4,8,9,15,17,19,22,23,len(pdf)-1]:
        if i<len(pdf):
            pdf[i].get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(folder/f'page_{i+1:03d}.png')
    texts=[p.get_text() for p in pdf]
    appendix=next(i for i,t in enumerate(texts) if '\n附录\n' in t)
    report={'pages':len(pdf),'abstract_pages':1 if '1 问题重述' in texts[1] else None,
            'main_pages_including_abstract':appendix,'body_pages_excluding_abstract':appendix-1,
            'outside_margin_words':outside,'pdf_bytes':(OUT/'qa/rendered/final_paper.pdf').stat().st_size}
    (folder/'layout_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))


if __name__=='__main__':
    main()
