import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .pagespeedinsightseo import output_handler as pss
from .robotparser import output_handler as robotparser

# Runs all SEO tool tests and return a dict with all the desired output
def run_test(url):
    output = {}

    # PAGESPEED INSIGHT SEO --------------------------------------------------------- #
    print("\'PageSpeed Insight SEO\' test started.")
    output["pagespeed_seo"], robot_valid = pss.get_output(url)
    print("Test ended\n")

    # ROBOT PARSER ------------------------------------------------------------------ #    
    print("\'Robot parser\' test started.")
    output["robot_parser"] = robotparser.get_output(url, robot_valid)
    print("Test ended\n")


    return output
