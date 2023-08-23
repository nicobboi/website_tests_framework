import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .mauve import output_handler as mauve

def run_test(url):
    output = {}

    # if the env var is set, start only the mockup test
    if os.environ.get("MOCKUP_TESTS"):
        print("'Mockup' test started.")
        output["accessibility-mockup"] = mockup.get_output(url, min_score=67, max_score=100)
        print("Test ended.\n")
        return output  

    # MAUVE++ -------------------------------------------------------------------- #
    print("\'Mauve++\' test started.")
    output["mauve++"] = mauve.get_output(url)
    print("Test ended.\n")


    return output