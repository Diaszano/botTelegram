#!/bin/bash
pyinstaller \
--clean \
--console  \
--additional-hooks-dir='./' \
--distpath=linuxdist \
--workpath=temporario \
--specpath=temporario \
main.py \
--onefile \
--name bot_telegram.dzn
rm -r ./temporario/
clear
echo "Cridado o executavel bot_telegram.dzn"