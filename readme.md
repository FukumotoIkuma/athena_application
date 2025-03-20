# How to build

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