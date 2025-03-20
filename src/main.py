from import_xlsx import read_excel_to_table, create_medical_report_df
from write_to_pdf import write_application_pdf
import db_columns as db_cols
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
def main():
    # Replace 'example.xlsx' with the path to your Excel file
    excel_file_path = 'R6アテナ診療請求書【1回】0425.xlsm'
    df_dict = read_excel_to_table(excel_file_path)
    medical_report_df = create_medical_report_df(df_dict)
    # print(medical_report_df)

    writer = PdfWriter()

    for index, row in medical_report_df.iterrows():
        date = row[db_cols.date].strftime('%Y-%m-%d')
        horse_name = row[db_cols.horse_name]
        horse_gender = row[db_cols.horse_gender]
        horse_color = row[db_cols.horse_color]
        horse_age = row[db_cols.horse_age]
        owner_name = row[db_cols.owner_name]
        stable_name = row[db_cols.stable_name]
        diagnosis = row[db_cols.diagnosis]
        page = write_application_pdf(date,
                             horse_name,
                             horse_gender,
                             horse_color,
                             horse_age,
                             owner_name,
                             stable_name,
                             diagnosis)
        writer.add_page(page)

    # 出力は実行した時間をファイルに含める
    # TODO 開発中はファイル上書きのため、ファイル名を固定にしている
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    # output_pdf = f"output/診療申込書_{now}.pdf"
    output_pdf = f"output/診療申込書_更新版.pdf"


    # 新しいPDFを保存
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    main()