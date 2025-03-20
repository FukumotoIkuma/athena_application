# pyinstallerのおまじない
import pypdf
import reportlab
import pandas
# 以下のコードは、Flaskとwebviewを使ってGUIアプリケーションを作成するためのコード
import os
import webview
from flask import Flask, render_template, request
import shutil
import main
import sys

# ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.'
# TEMPLATES_PATH = ROUTE_PATH + '/templates'

# app = Flask(name, template_folder=TEMPLATES_PATH)


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # ここでエラーが発生した場合、スクリプトを強制的に終了する
        sys.exit(f"An error occurred while rendering the template: {e}")
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        assert 'file' in request.files, "ファイルが選択されていません"
        file = request.files['file']
        assert file.filename != '', "ファイルが選択されていません"
        assert file.filename.endswith(('.xlsx', '.xlsm')), "ファイル形式が間違っています"
    except AssertionError as e:
        return render_template('index.html', message=e)
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        try:
            main.main(file_path)
        except Exception as e:
            return render_template('index.html', message=f"不明なエラー: {e}")

        return render_template('index.html', message=f"変換完了. ダウンロードフォルダを確認してください")
if __name__ == '__main__':
    # Flaskアプリケーションをバックグラウンドで実行
    from threading import Thread
    port = 5001
    thread = Thread(target=lambda: app.run(port=port,debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()

    # Webviewウィンドウを起動
    webview.create_window("診療申込書作成アプリ", f"http://localhost:{port}")
    webview.start()

    # uploadフォルダ内のファイルを削除
    
    shutil.rmtree(UPLOAD_FOLDER)
