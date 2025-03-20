import os
import webview
from flask import Flask, render_template, request
import shutil
import src.main as main
app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', message="ファイルが選択されていません")
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message="ファイルが選択されていません")
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        main.main(file_path)

        return render_template('index.html', message=f"変換完了. ダウンロードフォルダを確認してください")
if __name__ == '__main__':
    # Flaskアプリケーションをバックグラウンドで実行
    from threading import Thread
    thread = Thread(target=lambda: app.run(debug=True, port=65339, use_reloader=False))
    thread.daemon = True
    thread.start()

    # Webviewウィンドウを起動
    webview.create_window("診療申込書作成アプリ", "http://localhost:65339")
    webview.start()

    # uploadフォルダ内のファイルを削除
    
    shutil.rmtree(UPLOAD_FOLDER)
