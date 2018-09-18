from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

import datetime
import json
import os
import sys

client = MongoClient(os.environ['MONGODB_URI'])
app = Flask(__name__, static_url_path='')


def get_5_last_documents():
    return list(client.get_database().coll.find().sort("ts", -1).limit(5))


@app.route('/add_document', methods=['POST'])
def add_document():
    error_msg = None

    try:
        document = json.loads(request.form['document'])
        document["ts"] = str(datetime.datetime.now())
    except Exception as e:
        error_msg = "Converting to JSON failed: {}".format(e)

    if not error_msg:
        try:
            client.get_database().coll.insert(document)
        except Exception as e:
            error_msg = "Inserting into MongoDB failed: {}".format(e)

    return redirect(url_for(
        'index',
        msg=error_msg or "Document successfully added",
        notification=True,
        success=not(bool(error_msg))
    ))


@app.route('/delete_doc', methods=['GET'])
def delete_doc():
    error_msg = None
    oid = request.args.get('oid')

    try:
        client.get_database().coll.delete_one({"_id": ObjectId(oid)})
    except Exception as e:
        error_msg = "Deletion of object failed: {}".format(e)

    return redirect(url_for(
        'index',
        msg=error_msg or "{} successfully deleted".format(oid),
        notification=True,
        success=not(bool(error_msg))
    ))


@app.route('/')
def index():
    notification = request.args.get('notification') == 'True'
    success = request.args.get('success') == 'True'
    msg = request.args.get('msg')
    results = get_5_last_documents()
    return render_template(
        "index.html",
        results=results,
        notification=notification,
        success=success,
        msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
