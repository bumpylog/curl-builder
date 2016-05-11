from flask import Flask
from flask import render_template, send_file, url_for, abort
from flask.ext.pymongo import PyMongo
from flask import request, jsonify
from datetime import datetime
from random import randint
import json
import bson
from bson.json_util import dumps
from flask import redirect
app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
@app.route('/<int:code>', methods=['GET'])
def hello_world(code):
    if request.method == 'GET':
        return render_template("index.html")

@app.route('/saveSnippet', methods=['POST'])
def saveSnippet():
    data = request.get_json()
    data['randInt'] = randint(100000, 999999)
    print data
    curlCommandDb = mongo.db.savedCurls.insert_one(data).inserted_id
    print curlCommandDb
    print mongo.db.savedCurls.count()
    return json.dumps({'code': data.get("randInt")});

#Write an endpoint /<abc123> that searches for the code in the collection and returns
#it to the client which then displays it in the form.
@app.route('/retrieveSnippet/<int:code>', methods=['POST'])
def loadCurl(code):
    if request.method == 'POST':
        print code
        curl = mongo.db.savedCurls.find_one({"randInt": code})
        return bson.json_util.dumps(curl)

if __name__ == '__main__':
    app.run(debug=True)
