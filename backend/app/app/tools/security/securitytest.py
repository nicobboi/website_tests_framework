# import here the output handlers
from ..toolmockup import output_handler as mockup
from .shcheck import output_handler as shcheck
from .ssllabsscan import output_handler as ssllabscan

# Runs all SECURITY tool tests and return a dict with all the desired output
def run_test(url):
    # insert here the name of the tools used
    output = {
        "security-mockup": None,
        # "sh-check": None,
        # "ssllabs-scan": None
    }

    # SHCHECK -------------------------------------------------------------------- #

    # print("\'Security headers check\' test started.")

    # output["sh-check"] = shcheck.get_output(url)

    # print("Test ended.\n")
    
    # SSLLABS-SCAN --------------------------------------------------------------- #

    # print("\'SSLlabs-scan\' test started.")

    # output["ssllabs-scan"] = ssllabscan.get_output(url)

    # print("Test ended.\n")

    # MOCKUP --------------------------------------------------------------------- #

    print("\'Mockup\' test started.")

    output["security-mockup"] = mockup.get_output(url, min_score=75, max_score=100)

    print("Test ended.\n")
    
    # ----------------------------------------------------------------------------- #

    return output


