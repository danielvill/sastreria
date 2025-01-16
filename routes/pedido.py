from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.pedido import Pedido
from pymongo import MongoClient
db = dbase()
pedido = Blueprint('pedido', __name__)
