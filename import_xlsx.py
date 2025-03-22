import pandas as pd
import db_columns as db_cols

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

    medical_report_df:pd.DataFrame = df_dict[db_cols.medical_record]
    # 先頭行から順に削除し、カラム名の行になったところで削除を終了する
    # 現行の複数カラム分で条件判定する（今後の変更にも程度対応できるように）
    cols = ["伝票番号", "診療日", "本当の診察日", "該当期間", "開始", "終了", "支払", "馬名"]

    for i in range(min(len(medical_report_df), 10 ** 2)):
        part_of_row = medical_report_df.iloc[i][2: 2 + len(cols)]

        same_check_value = sum([cols[i] == part_of_row.iloc[i] for i in range(len(cols))])
        if same_check_value > 2:
            medical_report_df = medical_report_df.drop(list(range(i)))
            break
    else:
        raise Exception("カルテシートに予想外の変更が加えられています")
    # 先頭行をカラム名にする
    medical_report_df.columns = medical_report_df.iloc[0]

    # A列のカラム名を変更
    medical_report_df.columns = [db_cols.use] + list(medical_report_df.columns[1:])

    # useカラムに値があるrecordのみを抽出
    medical_report_df = medical_report_df[medical_report_df[db_cols.use].notnull()]
    # print(medical_report_df)

    # useカラムの値を数字に変換できないものは削除
    medical_report_df = medical_report_df[
        medical_report_df[db_cols.use].apply(lambda x: str(x).isnumeric() if pd.notnull(x) else False)
    ]

    # print(medical_report_df)

    # 日付・馬名・性別・毛色・生年月日・馬主名・厩舎名・診断のカラムをだけに絞り込む
    medical_report_df = medical_report_df[
        [db_cols.date, db_cols.horse_name, db_cols.horse_gender, 
         db_cols.horse_color, db_cols.horse_age, db_cols.owner_name, 
         db_cols.stable_name, db_cols.diagnosis]]
    
    # 日付をdatetime型に変換
    medical_report_df[db_cols.date] = pd.to_datetime(medical_report_df[db_cols.date], errors='coerce')
    
    return medical_report_df
# Example usage
if __name__ == "__main__":
    # Replace 'example.xlsx' with the path to your Excel file
    excel_file_path = 'R6アテナ診療請求書【1回】0425.xlsm'
    tables = read_excel_to_table(excel_file_path, "カルテ")
    
    if len(tables) > 0:
        print(f"Successfully read {len(tables)} table(s) from the Excel file:")
        for table in tables.values():
            # print(table.attrs['sheet_name'])
            # print(table)
            pass
    else:
        print("No tables were read from the Excel file.")

    medical_report_df = create_medical_report_df(tables)
    print(medical_report_df)