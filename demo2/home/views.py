from home import home_blue


@home_blue.route('/')
def index():
    return 'index'
