#!/usr/bin/env bash

./geneaccrefine log.txt
./genelossrefine log.txt
python show_loss.py
python show_acc.py
