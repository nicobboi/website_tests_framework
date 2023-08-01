# import here the output handlers
from ..toolmockup import output_handler as mockup
from .pagespeedinsightseo import output_handler as pss
from .robotparser import output_handler as robotparser

# Runs all SEO tool tests and return a dict with all the desired output
def run_test(uri):
    # tools's output returned
    output = {
        "seo-mockup": None,
        # "pagespeed_seo": None,
        # "robot_parser": None
    }

    # PAGESPEED INSIGHT SEO --------------------------------------------------------- #

    # print("\'PageSpeed Insight SEO\' test started.")

    # output["pagespeed_seo"], robot_valid = pss.get_output(uri)

    # print("Test ended\n")

    # ROBOT PARSER ------------------------------------------------------------------ #    

    # print("\'Robot parser\' test started.")

    # output["robot_parser"] = robotparser.get_output(uri, robot_valid)
    
    # print("Test ended\n")

    # MOCKUP --------------------------------------------------------------------- #

    print("\'Mockup\' test started.")

    output["seo-mockup"] = mockup.get_output(uri, min_score=15, max_score=56)

    print("Test ended.\n")

    # ------------------------------------------------------------------------------- #

    return output
