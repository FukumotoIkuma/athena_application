from django.views.generic import TemplateView
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import B6, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

class ReportlabView(TemplateView):
    def save(self):
        # 保存先のファイルパスを指定
        file_path = "example.pdf"
        self._create_pdf(file_path)
        return file_path

    def _draw_text(self, text:str, x:float, y:float, font='HeiseiKakuGo-W5', size=10.5,charSpace:float = 0, center = False):
        assert self.pdf_canvas, "pdf_canvas is not defined"
        self.pdf_canvas.setFont(font, size)
        if center:
            self.pdf_canvas.drawCentredString(x, y, text,charSpace=charSpace)
        else:
            self.pdf_canvas.drawString(x, y, text, charSpace=charSpace)
    
    def _create_pdf(self, file_path):
        # 診療報告書の計測結果は以下の通り
        # 横128mm 縦108mm + 76mm = 184 mm
        # おそらくこのサイズはB6(128mm × 182mm). 


        # 日本語が使えるゴシック体のフォントを設定する
        font_name = 'HeiseiKakuGo-W5'
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))


        # pdfを描く場所を作成：pdfの原点は左上にする(bottomup=False)
        pdf_canvas = canvas.Canvas(file_path,bottomup=False)  # ファイルパスを指定
        self.pdf_canvas = pdf_canvas

        # B6縦向きのサイズを指定
        width, height = B6
        pdf_canvas.setPageSize(portrait(B6))


        # title
        self._draw_text("診療申込書", width/2, 20 * mm, center=True, charSpace=3 * mm)

        # date
        wareki = 7
        MM = 8
        DD = 9
        self._draw_text(f"{wareki}年{MM}月{DD}日", width/2, 25 * mm, charSpace=3 * mm)

        # clinic
        self._draw_text("Athena Integrative Veterinary Care", 10 * mm, 30 * mm, size = 8)
        self._draw_text("アテナ統合獣医ケア Ban'ei 競走馬診療所   様", 10 * mm, 35 * mm, size = 8)

        # trainer name
        self._draw_text("調教師", width/2, 45 * mm)
        pdf_canvas.line(width/2, 48 * mm, width - (10 * mm), 48 * mm)
        
        self._draw_text( "次の馬の診療をお願いいたします。", 10 * mm, 60 * mm)
        

        # horse name, horse age, horse gender, owner name, race date

        # Table structure
        table_x = 10 * mm
        table_y = 75 * mm
        row_height = 10 * mm

        # table Headers
        upper_headers = [
            ["馬名", ""],
            ["年齢", ""],
            ["性別", "オス　　　セン　　　メス"],
            ["馬主名", ""],
            ["出走予定日", "　　　月　　　日　　　未定"]
        ]
        col_widths = [30 * mm, width - 20*mm - 30*mm]

        for i, row in enumerate(upper_headers):
            for j, cell in enumerate(row):
                self._draw_text(cell, table_x + 10 + sum(col_widths[:j]), table_y + i * row_height - 10)
                pdf_canvas.rect(table_x + sum(col_widths[:j]), table_y + i * row_height, col_widths[j], -row_height)

        # horse color
        self._draw_text("毛色", table_x + 70 * mm, table_y + 1 * row_height - 10, charSpace=3 * mm)
        pdf_canvas.rect(table_x + 70 * mm - 1 * mm, table_y + 1 * row_height, 13 * mm, -row_height)

        # medical report, diagnosis, etc...
        row_heights = [
            1  * mm,
            5   * mm,
            5   * mm,
            10  * mm,
            5   * mm,
            15  * mm
        ]
        col_widths = [
            [width - 20 * mm],
            [width - 20 * mm],
            [width - 20 * mm - 30 * mm, 30 * mm],
            [width - 20 * mm - 30 * mm, 30 * mm],
            [width - 20 * mm - 60 * mm, 60 * mm],
            [width - 20 * mm - 60 * mm, 60 * mm],
        ]

        lower_headers = [
            [""],
            ["診療報告"],
            ["病名", "獣医師名"],
            ["", "福本"],
            ["規制・禁止薬物使用状況", "備考"],
            ["規制・禁止・未使用", ""]
        ]
        for i, _row_height in enumerate(row_heights):
            for j,_col_width in enumerate(col_widths[i]):
                pdf_canvas.rect(
                    table_x + sum(col_widths[i][:j]),
                    table_y + (len(upper_headers) -1) * row_height + sum(row_heights[:i+1]), 
                    _col_width, 
                    -_row_height
                    )
                self._draw_text(
                    lower_headers[i][j], 
                    table_x + sum(col_widths[i][:j]) + col_widths[i][j]/2, 
                    table_y + (len(upper_headers) -1) * row_height + sum(row_heights[:i+1]) - row_heights[i]/2 + 1.5 * mm, 
                    center=True
                    )
        pdf_canvas.line(table_x, table_y + (len(upper_headers) -1) * row_height, width - 10 * mm, table_y + (len(upper_headers) -1) * row_height)
        pdf_canvas.showPage()

        # pdfの書き出し
        pdf_canvas.save()


if __name__ == "__main__":
    view = ReportlabView()
    view.save() 
