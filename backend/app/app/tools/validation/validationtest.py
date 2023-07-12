from subprocess import Popen, PIPE
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

def run_test(uri):
    output = {
        "pa-website-validator": None
    }

    script_dir = os.path.dirname(__file__) 

    # PA-WEBSITE-VALIDATOR ------------------------------------------------------- #

    pwv_path = script_dir + "/pa-website-validator/"
    out_fold = script_dir + "/pa-website-validator/reports/"

    print("\'pa-website-validator\' test started.")

    start_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    with Popen(["node", pwv_path + "dist", "--type", "municipality", "--destination", out_fold, "--report", "report", \
                          "--accuracy", "min", "--website", uri], stdout=PIPE, stderr=PIPE) as proc:
        proc.wait()

    end_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    with open(out_fold + "report.json", "r") as f:
        pwt_out = json.load(f)

        mc_score = int(pwt_out['categories']['modelComplianceInformation']['score'] * 100)
        rt_score = int(pwt_out['categories']['reccomandationsAndAdditionalTests']['score'] * 100)

        output['pa-website-validator'] = {
            "scores": {
                "modelcompliance_score": mc_score,
                "reccomandationstests_score": rt_score
            },
            "notes": None,
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": pwt_out
        }

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output