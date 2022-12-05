from flask import Blueprint

datamanager = Blueprint('datamanager', __name__)

from app.datamanager import router