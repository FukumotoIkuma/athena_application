# How to use

# pythonのインストール
「python install」などで導入。
python3.9を導入すること。

start.shに実行権限を与える

start.shを実行する


# pyinstallerを用いたexeファイル

はじめに、pyinstallerをビルドし直す必要がある
venv等の場合もほぼ同様

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