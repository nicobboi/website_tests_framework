import os
from ..toolmockup import output_handler as mockup

# import here the output handlers
from .pagespeedinsightperformance import output_handler as psp

def run_test(url):
    output = {}

    # if the env var is set, start only the mockup test
    if os.environ.get("MOCKUP_TESTS"):
        print("'Mockup' test started.")
        output["performance-mockup"] = mockup.get_output(url, min_score=67, max_score=100)
        print("Test ended.\n")
        return output        
    
    # PAGESPEED INSIGHT PERFOMANCE ----------------------------------------------- #
    print("\'PageSpeed Insight PERFORMANCE\' test started.")
    output["pagespeed_performance"] = psp.get_output(url)
    print("Test ended.\n")


    return output