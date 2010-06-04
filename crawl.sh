#!/bin/sh

mkdir -p $HOME/var/log
export SCRAPY_LOG_FILE=$HOME/var/log/scrapy_novel.log
python scrapy-ctl.py crawl qidian
