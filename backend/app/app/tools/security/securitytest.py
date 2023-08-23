import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .shcheck import output_handler as shcheck
from .ssllabsscan import output_handler as ssllabscan

# Runs all SECURITY tool tests and return a dict with all the desired output
def run_test(url):
    output = {}

    # if the env var is set, start only the mockup test
    if os.environ.get("MOCKUP_TESTS"):
        print("'Mockup' test started.")
        output["security-mockup"] = mockup.get_output(url, min_score=67, max_score=100)
        print("Test ended.\n")
        return output   

    # SHCHECK -------------------------------------------------------------------- #
    print("\'Security headers check\' test started.")
    output["sh-check"] = shcheck.get_output(url)
    print("Test ended.\n")
    
    # SSLLABS-SCAN --------------------------------------------------------------- #
    print("\'SSLlabs-scan\' test started.")
    output["ssllabs-scan"] = ssllabscan.get_output(url)
    print("Test ended.\n")


    return output


