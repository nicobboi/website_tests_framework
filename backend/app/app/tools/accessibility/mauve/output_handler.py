from subprocess import Popen
from datetime import datetime, timezone
import json
import os

def get_output(uri):
    # tool's script path
    mauve_path = "./index.js"
    # report download path
    output_path = "./reports"

    start_test_timestamp = str(datetime.now(tz=timezone.utc))

    with Popen(["node", mauve_path, uri, output_path]) as proc:
        proc.wait()

    end_test_timestamp = str(datetime.now(tz=timezone.utc))

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

        output = {
            "scores": {
                "overall": int(audits_passed / audits_total * 100),
            },
            "notes": str(audits_passed) + " audits passed on a total of " + str(audits_total),
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": mauve_out
        }

    os.remove(report_path)

    return output