# render_templateの動作がpyinstallerで不安定のため
# 規模の小さいアプリケーションであるので
# htmlを直接記述することにした
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>カルテのExcelをアップロード</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            height: 100vh;
        }
        header {
            background-color: #76a1cf;
            color: #fff;
            padding: 20px 40px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            font-size: 1.5rem;
        }
        main {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* 画面全体の高さ */
            position: relative;
        }
        h1 {
            color: #333;
            font-size: 2rem;
        }
        form {
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 1.2rem;
        }
        label {
            display: block;
            margin-bottom: 15px;
            font-weight: bold;
            font-size: 1.2rem;
        }
        input[type="file"] {
            margin-bottom: 20px;
            font-size: 1.1rem;
        }
        button {
            background-color: #007BFF;
            color: #fff;
            border: none;
            padding: 15px 30px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1.2rem;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            margin-top: 15px;
            color: rgb(0, 0, 0);
            font-size: 1.2rem;
        }
        .drop-zone {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 2px dashed #007BFF;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #007BFF;
            font-size: 1.5rem;
            visibility: hidden;
        }
        .drop-zone.active {
            visibility: visible;
            background-color: rgba(0, 123, 255, 0.1);
        }
    </style>
    <script>
        function showProcessingMessage() {
            const messageElement = document.querySelector('.message');
            if (messageElement) {
                messageElement.textContent = "処理中です。お待ちください...";
                messageElement.style.color = "orange";
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.querySelector('.drop-zone');
            const fileInput = document.querySelector('#file');

            window.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('active');
            });

            window.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropZone.classList.remove('active');
            });

            window.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('active');
                if (e.dataTransfer.files.length > 0) {
                    fileInput.files = e.dataTransfer.files;

                    // ドロップされたファイル名を表示
                    const messageElement = document.querySelector('.message');
                    if (messageElement) {
                        messageElement.textContent = `選択されたファイル: ${e.dataTransfer.files[0].name}`;
                        messageElement.style.color = "green";
                    }
                }
            });
        });
    </script>
</head>
<body>
    <!-- <header>
        <h1>カルテのExcelを選択してください</h1>
    </header> -->
    <div class="drop-zone"></div>
    <main>
        <div class="drop-zone">ここにファイルをドラッグ&ドロップ</div>
        <form action="/upload" method="post" enctype="multipart/form-data" onsubmit="showProcessingMessage()">
            <label for="file">ファイルを選択してください:</label>
            <input type="file" name="file" id="file">
            <button type="submit">変換</button>
            <!-- メッセージをアップロードフィールドの下に表示 -->
            <p class="message">
                {% if message %}
                    {{ message }}
                {% endif %}
            </p>
        </form>
        <div id="status"></div>
    </main>
</body>
</html>
"""