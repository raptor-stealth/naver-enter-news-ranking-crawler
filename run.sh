#!/bin/bash

PWD="/home/cpm0722/wd/naver-enter-news-ranking-crawler"

cd ${PWD}

OPENAI_API_KEY=""

OPENAI_API_KEY="${OPENAI_API_KEY}" /usr/bin/python3 dump.py >> ${PWD}/dump.log 2>&1
