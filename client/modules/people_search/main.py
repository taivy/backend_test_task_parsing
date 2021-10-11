from flask import Blueprint, current_app, render_template

from modules.people_search import forms, utils


people_search_bp = Blueprint('people_search', __name__)


@people_search_bp.route('/', methods=['get', 'post'])
def main_page():
    form = forms.PeopleSearchForm()
    if form.validate_on_submit():
        api_url = current_app.config["API_URL"]
        api_req_timeout = current_app.config["API_REQUESTS_TIMEOUT"]

        request_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'middle_initial': form.middle_initial.data,
            'state': form.state.data,
            'city': form.city.data,
        }

        result_link, error = utils.make_people_search_request_to_api(
            api_url, request_data, api_req_timeout)
        return render_template(
            'result_page.html', result_link=result_link, error_text=error)

    return render_template('main_page.html', form=form)
