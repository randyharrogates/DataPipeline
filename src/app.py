from pydoc import render_doc
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resource")
def resource():
    id = request.args.get('id')
    name = request.args.get('name')
    return render_template("index.html", template_id=id, template_name=name)


if __name__ == "__main__":
    app.run(debug=True)

# This should be = to mLab's URI for db connection
app.config['MONGO_URI'] = 'mongodb://...mlab.com:.../...'
# This should be = name of mongoDB database
app.config['MONGO_DBNAME'] = 'mytest'

mongo = PyMongo(app)
