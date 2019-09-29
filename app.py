import flask
from flask import Flask
from flask import request, render_template, jsonify

from db_processor import db_get_position, db_filter
from data_converter import list_to_dict

app = Flask(__name__)


@app.route("/ajax/get_position", methods=['GET', 'POST'])
def get_position():
        if request.method == 'GET':
                positions = db_get_position()
                return jsonify(positions)

@app.route('/ajax/filter', methods=['GET', 'POST'])
def filter():
        if request.method == 'GET':
                position = request.args.get('position')
                return jsonify(db_filter(position))


                





                

if __name__ == "__main__":
        app.run()
