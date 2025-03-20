#encoding: utf-8

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import B6
from io import BytesIO

# 診療申込書.pdfを読み込み、書き込む
def add_text_to_pdf(input_pdf_path, output_pdf_path, text, x, y):
    # 日本語フォントを登録
    font_name = 'HeiseiKakuGo-W5'
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    # 元のPDFを読み込む
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        # 新しいPDFページにテキストを描画
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=B6)
        can.setFont(font_name, 12)
        can.drawString(x, y, text)
        can.save()

        # テキストを描画したPDFを読み込み
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # 元のページにテキストをマージ
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    # 新しいPDFを保存
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

# 使用例
if __name__ == "__main__":
        
    input_pdf = "data/診療申込書.pdf"
    output_pdf = "output/診療申込書_更新版.pdf"
    add_text_to_pdf(input_pdf, output_pdf, "追加するテキスト", 10, 10)
