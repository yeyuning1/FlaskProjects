from user_select import db


def select_write_db(f):

    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return f(*args, **kwargs)

    return wrapper


def select_read_db(f):
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return f(*args, **kwargs)

    return wrapper