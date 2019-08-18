from flask import Blueprint

home_blue = Blueprint('home_b', __name__, url_prefix='/home')
from . import views
