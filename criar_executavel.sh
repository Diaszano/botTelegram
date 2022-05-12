#!/bin/bash
pyinstaller --console --clean --distpath=linuxdist --workpath=temporario main.py --onefile --name bot_telegram.dzn
rm -r *.spec
rm -r ./__pycache__/
cp ./linuxdist/* ./
rm -r ./temporario/
rm -r ./linuxdist/
clear
echo "Cridado o executavel bot_telegram.dzn"