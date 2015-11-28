#coding=utf-8
from flask import Blueprint
__author__ = 'archer'

auth = Blueprint('auth', __name__)

from . import views
