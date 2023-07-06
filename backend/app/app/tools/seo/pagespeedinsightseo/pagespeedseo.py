import requests

# Runs the PageSpeed Insight's API for SEO testing on the given URL
# Returns a JSON with all the data
def test(uri):
    # API's url for the GET request
    url = "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed"

    # params to send with the GET request
    params = {
        "category": "SEO",
        "url": uri,
    }

    # request to PageSpeed Insight and returns a JSON
    res = requests.get(url, params=params)
    output = res.json()

    # return directly the content of the JSON and the path of the report file
    return output

