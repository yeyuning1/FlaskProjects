from flask import Blueprint

home_blu = Blueprint('home_b', __name__, url_prefix='/home')
from .views import *
