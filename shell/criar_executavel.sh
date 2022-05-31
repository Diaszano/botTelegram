#!/bin/bash
pyinstaller \
--clean \
--console  \
--distpath=executavel \
--workpath=temporario \
--specpath=temporario \
main.py \
--onefile \
--name bot_telegram.dzn
rm -r ./temporario/
clear
echo "Cridado o executavel bot_telegram.dzn"