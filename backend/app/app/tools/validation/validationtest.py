import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .pawebsitevalidator import output_handler as pwv

def run_test(url):
    output = {}

    # if the env var is set, start only the mockup test
    if os.environ.get("MOCKUP_TESTS"):
        print("'Mockup' test started.")
        output["validation-mockup"] = mockup.get_output(url, min_score=67, max_score=100)
        print("Test ended.\n")
        return output    


    # PA-WEBSITE-VALIDATOR ------------------------------------------------------- #
    print("\'pa-website-validator\' test started.")
    output["pa-website-validator"] = pwv.get_output(url)
    print("Test ended.\n")


    return output