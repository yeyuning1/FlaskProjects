class CeleryConfig(object):
    """
    Celery默认配置
    """
    broker_url = 'amqp://guest:guest@192.168.105.128:5672'  # 消息队列的地址


    task_routes = {  # 任务路由
        'sms.*': {'queue': 'sms'},
    }

    # 阿里短信服务
    DYSMS_ACCESS_KEY_ID = ''
    DYSMS_ACCESS_KEY_SECRET = ''