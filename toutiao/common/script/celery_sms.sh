#! /bin/bash
source ~/.bash_profile
cd /home/python/toutiao-backend/common
workon toutiao
exec celery -A celery_tasks.main worker -l info -Q sms