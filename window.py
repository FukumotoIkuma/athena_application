# pyinstallerのおまじない
import pypdf
import reportlab
import pandas


from flask import Flask, request, render_template_string
import os
import shutil
import webview
import threading

import main
from html_template import HTML_TEMPLATE

app = Flask(__name__)

import os
import sys

if getattr(sys, 'frozen', False):
    # PyInstaller の場合（--onefile で一時フォルダに展開される）
    BASE_DIR = sys._MEIPASS
else:
    # 通常の Python 実行時
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Application directory:", BASE_DIR)


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # dir構造を把握するため一時的にここで表示する
    # base_dirで何が表示されるか確認する
    dir = os.listdir(BASE_DIR)
    return render_template_string(HTML_TEMPLATE, message= f"{dir}")
   
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        assert 'file' in request.files, "ファイルが選択されていません"
        file = request.files['file']
        assert file.filename != '', "ファイルが選択されていません"
        assert file.filename.endswith(('.xlsx', '.xlsm')), "ファイル形式が間違っています"
    except AssertionError as e:
        return render_template_string(HTML_TEMPLATE, message= f"{e}")
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        try:
            main.main(file_path)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, message= f"不明なエラー: {e}")

        return render_template_string(HTML_TEMPLATE, message="変換完了. ダウンロードフォルダを確認してください")
    

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