import requests  # type: ignore


def get_callback(url, json):
    status_code = 500
    try:
        response = requests.post(url, json=json)
        result = str(response.status_code) + " HTTP\n"
        result += response.text
        status_code = response.status_code
        if response.status_code != 200:
            result = str(response.status_code) + " HTTP\n"
    except ConnectionError:
        result = "NO RESPONE"

    return result, status_code
