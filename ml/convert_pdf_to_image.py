
import fitz
pdffile = "os_3.pdf"
doc = fitz.open(pdffile)
zoom = 4
mat = fitz.Matrix(zoom, zoom)
val = f"sumnail.png"
page = doc.load_page(0)
pix = page.get_pixmap(matrix=mat)
pix.save(val)
doc.close()
