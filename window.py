import os
import webview
from flask import Flask, render_template, request

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
        return "ファイルが選択されていません", 400
    file = request.files['file']
    if file.filename == '':
        return "ファイル名が空です", 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return f"ファイル {file.filename} をアップロードしました"

if __name__ == '__main__':
    # Flaskアプリケーションをバックグラウンドで実行
    from threading import Thread
    thread = Thread(target=lambda: app.run(debug=True, port=65339, use_reloader=False))
    thread.daemon = True
    thread.start()

    # Webviewウィンドウを起動
    webview.create_window("ファイルアップロードアプリ", "http://localhost:65339")
    webview.start()
