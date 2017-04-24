
from flask import Flask
from flask import jsonify
from flask import request
from n4j import N4J

app = Flask(__name__)
n4jinstance = N4J("http://neo4j:admin@localhost:7474")

"""
export FLASK_APP=`pwd`/api.py
export FLASK_DEBUG=1
flask run
"""


@app.route('/ping/', methods=['GET'])
def get_ping():
    return "pong"


@app.route('/fof/', methods=['GET'])
def get_fof():
    """
    Checks if two users are of 2nd degree connection
    http://127.0.0.1:5000/fof/?ourid1=1&ourid2=3
    """
    args = request.args
    ourid1 = args['ourid1']
    ourid2 = args['ourid2']
    return jsonify({'result' : n4jinstance.is_fof(ourid1, ourid2) })


@app.route('/fofof/', methods=['GET'])
def get_fofof():
    """
    Checks if two users are of 2nd or 3rd degree connection
    http://127.0.0.1:5000/fofof/?ourid1=1&ourid2=3
    """
    args = request.args
    ourid1 = args['ourid1']
    ourid2 = args['ourid2']
    return jsonify({'result' : n4jinstance.is_fofof(ourid1, ourid2) })


@app.route('/2nd3rd/', methods=['GET'])
def get_2nd_or_3rd():
    """
    Returns all 2nd or 3rd degree connections for a user
    http://127.0.0.1:5000/2nd3rd/?ourid=3
    """
    args = request.args
    ourid = args['ourid']
    return jsonify({'result' : n4jinstance.get_2nd_or_3rd(ourid) })
