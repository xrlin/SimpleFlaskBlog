from flask import Blueprint
__author__ = 'archer'

main = Blueprint('main', __name__)

from . import views
