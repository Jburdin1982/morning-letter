import sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
src, out = sys.argv[1], sys.argv[2]
r = PdfReader(src); w = PdfWriter()
W, H = 612, 792
def bg(path):
    c = canvas.Canvas(path, pagesize=(W,H))
    c.setFillColor(HexColor('#f7f0dd')); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setStrokeColor(HexColor('#8a6a35'))
    c.setLineWidth(1.8); c.rect(22,22,W-44,H-44,stroke=1,fill=0)
    c.setLineWidth(0.6); c.rect(28,28,W-56,H-56,stroke=1,fill=0)
    c.save()
bg('/tmp/bg.pdf')
for pg in r.pages:
    b = w.add_page(PdfReader('/tmp/bg.pdf').pages[0])
    b.merge_page(pg)
w.write(out)
