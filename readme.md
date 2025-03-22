# How to use

## スクリプトのダウンロード
ブラウザで以下のURLにアクセスし、エクセルファイルのあるフォルダに解凍する
https://github.com/FukumotoIkuma/athena_application/archive/refs/heads/main.zip


## pythonのインストール
「python install」などで導入。
python3.9を導入すること。

## 必要なモジュールのインストール
展開したフォルダに移動し以下を実行
pip install -r requirements.txt

## ファイルの実行
python3 window.py



# pyinstallerを用いたexeファイル

はじめに、pyinstallerをビルドし直す必要がある

gitをインストールしておく必要がある。

venv等の環境の場合もほぼ同様

```bash
git clone https://github.com/pyinstaller/pyinstaller.git

cd pyinstaller/bootloader
python ./waf distclean all

pip install wheel

cd pyinstaller
pip install .

```

```bash
pyinstaller window.spec
```

bin/MTA_creation.exeを実行することで使える