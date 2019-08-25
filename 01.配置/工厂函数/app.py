from flask import Flask
from .create_app import create_app

app = create_app('dev')
