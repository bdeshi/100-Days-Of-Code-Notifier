#!/bin/sh
cd "$(dirname "$(realpath "$0")")" || exit
pipenv --bare run python notifier.py
