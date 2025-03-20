#encoding: utf-8

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import B6
from io import BytesIO
from datetime import datetime
import pandas as pd

# 診療申込書.pdfを読み込み、複数箇所にテキストを書き込む
def add_texts_to_pdf(font_name, reader:PdfReader, texts_with_positions):
  
    for page in reader.pages:
        # 新しいPDFページに複数のテキストを描画
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=B6)
        can.setFont(font_name, 12)
        for text, (x, y) in texts_with_positions:
            if pd.isna(text) or pd.isnull(text):
                text = ""
            can.drawString(x, y, str(text))
        can.save()

        # テキストを描画したPDFを読み込み
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # 元のページにテキストをマージ
        page.merge_page(new_pdf.pages[0])


def write_application_pdf(date, horse_name, horse_gender, horse_color, horse_age, owner_name, stable_name, diagnosis):

    # 日本語フォントを登録
    font_name = 'HeiseiKakuGo-W5'
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    # 元のPDFを読み込む
    input_pdf = "data/診療申込書.pdf"
    reader = PdfReader(input_pdf)
   

    # dateを整形
    # TODO ここでは雑な処理をしている
    year, month, day = date.split("-")
    date_y = 397
    # テキストを入力
    texts_with_positions = [
        (year, (167, date_y)),
        (str(int(month)), (235, date_y)),
        (str(int(day)), (275, date_y)),
        (horse_name, (90, 265)),
        (horse_color, (270, 240)),
        (horse_age, (130, 240)),
        (owner_name, (90, 193)),
        (stable_name, (230, 328)),
        (diagnosis, (40, 119)),
    ]
    add_texts_to_pdf(font_name, reader, texts_with_positions)


    # pdfの指定座標に楕円を描画
    gender_x = 0
    if horse_gender  == "牡":
        gender_x = 134
    elif horse_gender == "セン":
        gender_x = 191
    else:
        gender_x = 247

    gender_y = 213
    eclipse_width = 30
    eclipse_height = 18

    pos = (gender_x, gender_y, gender_x + eclipse_width, gender_y + eclipse_height)

    page = reader.pages[0]
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=B6)
    can.ellipse(pos[0], pos[1], pos[2], pos[3])
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    page.merge_page(new_pdf.pages[0])
    
    return page

# 使用例
if __name__ == "__main__":
    date = "2021-01-01"
    horse_name = "サイレンススズカ"
    horse_gender = "オス"
    horse_color = "栗"
    horse_age = "3"
    owner_name = "山田太郎"
    stable_name = "久田"
    diagnosis = "腹痛"

    page = write_application_pdf(date, horse_name, horse_gender, horse_color, horse_age, owner_name, stable_name, diagnosis)
    
    writer = PdfWriter()
    writer.add_page(page)

    # 出力は実行した時間をファイルに含める
    # TODO 開発中はファイル上書きのため、ファイル名を固定にしている
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    # output_pdf = f"output/診療申込書_{now}.pdf"
    output_pdf = f"output/診療申込書_更新版.pdf"


    # 新しいPDFを保存
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)
    print("診療申込書を作成しました。")