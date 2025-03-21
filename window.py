# pyinstallerのおまじない
import pypdf
import reportlab
import pandas


from flask import Flask, request, render_template
import os
import shutil
import webview
import threading

import main
import write_to_pdf

app = Flask(__name__)

import os
import sys

if getattr(sys, 'frozen', False):
    # PyInstaller の場合（--onefile で一時フォルダに展開される）
    # templatesなどの追加フォルダは、オプションで指定しないと含まれない
    #  .spec: datas=[('templates', 'templates'),('data','data')],
    BASE_DIR = sys._MEIPASS
    write_to_pdf.set_base_dir(BASE_DIR)
else:
    # 通常の Python 実行時
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

print("Application directory:", BASE_DIR)


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")
   
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        assert 'file' in request.files, "ファイルが選択されていません"
        file = request.files['file']
        assert file.filename != '', "ファイルが選択されていません"
        assert file.filename.endswith(('.xlsx', '.xlsm')), "ファイル形式が間違っています"
    except AssertionError as e:
        return render_template("index.html", message= f"{e}")
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        try:
            main.main(file_path)
        except Exception as e:
            return render_template("index.html", message= f"不明なエラー: {e}")

        return render_template("index.html", message="変換完了. ダウンロードフォルダを確認してください")
    

if __name__ == '__main__':
    # このportでアプリケーションを起動
    port = 5004

    # なんらかの原因でアプリケーションが終了しなかった場合に備えて
    # このportで起動してるアプリケーションを強制終了
    os.system(f"lsof -i:{port} | grep LISTEN | awk '{{print $2}}' | xargs kill")
    

    # debug= Trueだとコンパイル時にエラーが出る
    thread = threading.Thread(target=app.run, kwargs={'port': port, 'debug': False, 'use_reloader': False})
    thread.daemon = True
    thread.start()

    # Webviewウィンドウを起動
    webview.create_window("診療申込書作成アプリ", f"http://localhost:{port}")
    webview.start()


    # uploadフォルダ内のファイルを削除
    shutil.rmtree(UPLOAD_FOLDER)