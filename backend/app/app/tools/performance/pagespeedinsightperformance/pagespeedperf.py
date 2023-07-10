import requests

def test(uri):
    # API's url for the GET request
    url = "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed"

    # params to send with the GET request
    params = {
        "category": "PERFORMANCE",
        "url": uri,
    }

    # request to PageSpeed Insight and returns a JSON
    res = requests.get(url, params=params)
    output = res.json()

    # return directly the content of the JSON
    return output

