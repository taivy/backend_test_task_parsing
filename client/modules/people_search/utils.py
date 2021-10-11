import requests
from json.decoder import JSONDecodeError


def make_people_search_request_to_api(api_url, request_data, timeout=120):
    """
    Makes request to API, returns tuple (*result*, *error*)
    """
    try:
        response = requests.post(
            api_url + "/api/search_people", data=request_data, timeout=timeout)

        if response.status_code == 404:
            return None, None
        if response.status_code != 200:
            return None, f"Status code: {response.status_code}, message: {response.text}"

        try:
            resp_json = response.json()
        except JSONDecodeError as e:
            return None, f"JSON decode error: {e}"

        if not resp_json.get("result_link"):
            return None, f"No link in response from API"

        return resp_json["result_link"], None

    except requests.exceptions.Timeout:
        return None, "Timeout making request to API"
    except requests.exceptions.ConnectionError as err:
        return None, f"Connection error making request to API: {err}"
    except requests.exceptions.HTTPError as err:
        return None, f"Request to API failed: {err}"
