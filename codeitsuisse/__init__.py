from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.square
import codeitsuisse.routes.saladSpree
import codeitsuisse.routes.inventory
import codeitsuisse.routes.socialDistancing
import codeitsuisse.routes.fruitbasket
import codeitsuisse.routes.cleanFloor