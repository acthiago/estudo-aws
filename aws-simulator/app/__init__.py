from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Configurar a conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['aws_simulator']

from app import routes
