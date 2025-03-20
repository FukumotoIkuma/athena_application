import pandas as pd
import db_columns as db_cols
from datetime import datetime, timedelta

# Excelの日付シリアルをPythonの日付に変換する関数
def excel_date_to_python(excel_date):
    # Excelの日付は1900年1月1日を基準にしています
    excel_start_date = datetime(1900, 1, 1)
    delta = timedelta(days=excel_date - 2)  # Excelの誤差修正
    return excel_start_date + delta

def read_excel_to_table(file_path, *sheet_name_args):
    """
    Reads an Excel file and loads its content into a pandas DataFrame.

    :param file_path: The path to the Excel file.
    :param sheet_name_args: The name(s) of the sheet(s) to read from the Excel file.
    :return: A list of pandas DataFrames containing the content of the Excel file.
    """
    try:
        # Read the Excel file
        # sheet_name_args が指定されていない場合は、全てのシートを読み込む
        if not sheet_name_args:
            # エクセルファイルからシート名を取得する
            xls = pd.ExcelFile(file_path)
            sheet_name_args = xls.sheet_names
    
        result = {}
        # 指定されたシートをそれぞれ別のDataFrameに読み込む
        for sheet_name in sheet_name_args:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df.attrs['sheet_name'] = sheet_name
            result[sheet_name] = df
        return result

    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

# excelから読み込んだ複数のdfから診療報告書用tableを作成する関数
def create_medical_report_df(df_dict):
    """
    診療報告書用のtableを作成する関数
    """
    # 診療報告書用のtableを作成
    
    # カルテtableをベースのtableとしてコピー
    medical_report_df = df_dict[db_cols.medical_record].copy()

    # 馬名カラムはエクセル上の関数でDB参照により入力されているので削除
    medical_report_df = medical_report_df.drop(db_cols.horse_name, axis=1)

    # 日付・馬ID・診断のカラムをだけに絞り込む
    # medical_report_df = medical_report_df[[db_cols.date, db_cols.horse_id, db_cols.diagnosis]]

    horse_df = df_dict[db_cols.horse_db]

    # カルテと馬DBを結合
    medical_report_df = medical_report_df.merge(horse_df, on=db_cols.horse_id,)

    # 厩舎DBを結合
    medical_report_df = medical_report_df.merge(df_dict[db_cols.stable_db], on=db_cols.horse_stable_id)

    # 馬主DBを結合
    medical_report_df = medical_report_df.merge(df_dict[db_cols.owner_db], on=db_cols.horse_owner_id)

    # 日付・馬名・性別・毛色・生年月日・馬主名・厩舎名・診断のカラムをだけに絞り込む
    print(medical_report_df.columns)
    medical_report_df = medical_report_df[
        [db_cols.date, db_cols.horse_name, db_cols.horse_gender, 
         db_cols.horse_color, db_cols.horse_birth_date, db_cols.owner_name, 
         db_cols.stable_name, db_cols.diagnosis]]
    
    # 日付をdatetime型に変換
    medical_report_df[db_cols.date] = medical_report_df[db_cols.date].apply(excel_date_to_python)
    
    return medical_report_df
# Example usage
if __name__ == "__main__":
    # Replace 'example.xlsx' with the path to your Excel file
    excel_file_path = 'example.xlsx'
    tables = read_excel_to_table(excel_file_path)
    
    if len(tables) > 0:
        print(f"Successfully read {len(tables)} table(s) from the Excel file:")
        for table in tables.values():
            print(table.attrs['sheet_name'])
            print(table)
    else:
        print("No tables were read from the Excel file.")

    medical_report_df = create_medical_report_df(tables)
    print(medical_report_df)