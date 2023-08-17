from subprocess import Popen, PIPE
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# import here the output handlers
from ..toolmockup import output_handler as mockup

def run_test(url):
    output = {
        "validation-mockup": None,
        # "pa-website-validator": None
    }

    # script_dir = os.path.dirname(__file__) 

    # PA-WEBSITE-VALIDATOR ------------------------------------------------------- #

    # pwv_path = script_dir + "/pa-website-validator/"
    # out_fold = script_dir + "/pa-website-validator/reports/"

    # print("\'pa-website-validator\' test started.")

    # start_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    # with Popen(["node", pwv_path + "dist", "--type", "municipality", "--destination", out_fold, "--report", "report", \
    #                       "--accuracy", "min", "--website", url], stdout=PIPE, stderr=PIPE) as proc:
    #     proc.wait()

    # end_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    # with open(out_fold + "report.json", "r") as f:
    #     pwt_out = json.load(f)

    #     mc_score = int(pwt_out['categories']['modelComplianceInformation']['score'] * 100)
    #     rt_score = int(pwt_out['categories']['reccomandationsAndAdditionalTests']['score'] * 100)

    #     output['pa-website-validator'] = {
    #         "scores": {
    #             "modelcompliance_score": mc_score,
    #             "reccomandationstests_score": rt_score
    #         },
    #         "notes": None,
    #         "start_test_timestamp": start_test_timestamp,
    #         "end_test_timestamp": end_test_timestamp,
    #         "json_report": pwt_out
    #     }

    # print("Test ended.\n")

    # MOCKUP --------------------------------------------------------------------- #

    print("\'Mockup\' test started.")

    output["validation-mockup"] = mockup.get_output(url, min_score=35, max_score=90)

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output