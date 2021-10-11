import os

from flask import Blueprint, jsonify, make_response, request
from flask_cors import cross_origin

from parser import get_search_results


api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/search_people', methods=['post'])
@cross_origin()
def search_people():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    middle_initial = request.form.get('middle_initial')
    city = request.form.get('city')
    state = request.form.get('state')

    general_results_page_flag = (str(os.environ.get(
        "RETURN_ONLY_GENERAL_RESULTS_PAGE", False))).lower() == "true"

    result_link = get_search_results(
        first_name=first_name,
        last_name=last_name,
        middle_initial=middle_initial,
        city=city,
        state=state,
        general_results_page=general_results_page_flag,
    )
    if not result_link:
        return make_response(jsonify({}), 404)

    return make_response(jsonify({"result_link": result_link}))
