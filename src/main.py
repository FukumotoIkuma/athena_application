from src.import_xlsx import read_excel_to_table, create_medical_report_df
from src.write_to_pdf import write_application_pdf
import src.db_columns as db_cols

from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import os
def main(excel_file_path):
    # Replace 'example.xlsx' with the path to your Excel file
    try:
        df_dict = read_excel_to_table(excel_file_path)
    except Exception as e:
        raise Exception(f"ファイルに予定外の変更が加えられています")
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
    # ダウンロードフォルダに保存する
    download_folder = os.path.expanduser('~/Downloads')

    output_pdf = os.path.join(download_folder, f"診療申込書_{now}.pdf")


    # 新しいPDFを保存
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    main()