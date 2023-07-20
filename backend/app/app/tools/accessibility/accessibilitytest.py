from subprocess import Popen
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os
from glob import glob

def run_test(uri):
    output = {
        "mauve++": None
    }

    script_dir = os.path.dirname(__file__) 

    # MAUVE++ -------------------------------------------------------------------- #

    # tool's script path
    mauve_path = script_dir + "/mauve/index.js"
    # report download path
    output_path = script_dir + "/mauve/reports"

    print("\'Mauve++\' test started.")

    start_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    with Popen(["node", mauve_path, uri, output_path]) as proc:
        proc.wait()

    end_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    # if the url has '/' as last char, it will be removed
    if uri[-1] == '/':
        uri = uri[0:-1]
    # example: mauve-earl-reporthttps___www.comune.novellara.re.it
    report_path = output_path + "/mauve-earl-report" + uri.replace("/","_").replace(":","_") + ".json"

    # there's an error in the json (",]"), so I manually removed it
    replace_string = ""
    with open(report_path, "r") as f:
        replace_string = f.read()
    replace_string = replace_string.replace(",\n\t]", "\n\t]")
    with open(report_path, "w") as f:
        f.write(replace_string)

    with open(report_path, "r") as f:
        mauve_out = json.load(f)
        # compute the total number of audit passed compared to total audits
        audits_passed = len([x for x in mauve_out['@graph'] if x['earl:result']['dcterms:title'] == "PASS"])
        audits_total = len(mauve_out['@graph'])

        output['mauve++'] = {
            "scores": {
                "overall": int(audits_passed / audits_total * 100),
            },
            "notes": str(audits_passed) + " audits passed on a total of " + str(audits_total),
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": mauve_out
        }

    os.remove(report_path)

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output