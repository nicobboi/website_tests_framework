import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .pagespeedinsightseo import output_handler as pss
from .robotparser import output_handler as robotparser

# Runs all SEO tool tests and return a dict with all the desired output
def run_test(url):
    output = {}

    # if the env var is set, start only the mockup test
    if os.environ.get("MOCKUP_TESTS"):
        print("'Mockup' test started.")
        output["seo-mockup"] = mockup.get_output(url, min_score=34, max_score=78)
        print("Test ended.\n")
        return output   

    # PAGESPEED INSIGHT SEO --------------------------------------------------------- #
    print("\'PageSpeed Insight SEO\' test started.")
    output["pagespeed_seo"], robot_valid = pss.get_output(url)
    print("Test ended\n")

    # ROBOT PARSER ------------------------------------------------------------------ #    
    print("\'Robot parser\' test started.")
    output["robot_parser"] = robotparser.get_output(url, robot_valid)
    print("Test ended\n")


    return output
