from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.h_pedido import H_pedido
from pymongo import MongoClient
db = dbase()
h_pedido = Blueprint('h_pedido', __name__)
