# How to use

## スクリプトのダウンロード

ブラウザで以下のURLにアクセスし、zipファイルをダウンロード
https://github.com/FukumotoIkuma/athena_application/archive/refs/heads/main.zip

## スクリプトの解答

`V:\Users\user\`直下にファイルを解凍する
（この場所でないとショートカットが機能しません）

## pythonのインストール

「python install」などで検索し導入。
python3.9を導入すること。

## 必要なモジュールのインストール

展開したフォルダに移動し以下を実行
pip install -r requirements.txt

## ファイルの実行

python3 window.py
もしここで不要なモジュールがあった場合適宜pipを用いてインストール

## ショートカットを利用した起動

`MTFapp.vbs`を実行することでアプリケーションが起動する。このファイルのショートカットをデスクトップなどに追加すると良い。


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