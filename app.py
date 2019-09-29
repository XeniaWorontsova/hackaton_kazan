import flask
from flask import Flask
from flask import request, render_template, jsonify, db_get_costing_data, db_set_costing_data

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


@app.route('/ajax/get_costing_data', methods=['GET', 'POST'])
def get_costing_data():
        if request.method == 'GET':
                return jsonify(db_get_costing_data())


@app.route('/ajax/set_costing_data', methods=['GET', 'POST'])
def set_costing_data():
        if request.method == 'GET':
                vacancy_announcement_costs = request.args.get('vacancy_announcement_costs')
                payment_for_agency_services = request.args.get('payment_for_agency_services')
                reference_bonus = request.args.get('reference_bonus')
                hr_salary_costs = request.args.get('hr_salary_costs')
                db_set_costing_data(vacancy_announcement_costs, payment_for_agency_services, reference_bonus, hr_salary_costs)
                return flask.Response(status=200)


if __name__ == "__main__":
        app.run()
