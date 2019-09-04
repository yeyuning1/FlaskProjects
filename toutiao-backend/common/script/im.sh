#! /bin/bash
source ~/.bash_profile
export FLASK_ENV=production
cd /home/python/im/
workon toutiao
exec python main.py 8001