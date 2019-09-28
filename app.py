import flask
from flask import Flask
from flask import request, render_template, jsonify

from db_processor import db_get_position
from data_converter import list_to_dict

app = Flask(__name__)


@app.route("/ajax/get_position", methods=['GET', 'POST'])
def get_position():
        if request.method == 'POST':
                positions = db_get_position()
                return jsonify(positions)


if __name__ == "__main__":
        app.run()
