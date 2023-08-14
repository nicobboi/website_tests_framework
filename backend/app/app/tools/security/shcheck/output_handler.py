from subprocess import Popen, PIPE
from datetime import datetime, timezone
import json

def get_output(uri):
    shcheck_path = "./shcheck.py"

    start_test_timestamp = str(datetime.now(tz=timezone.utc))

    with Popen([shcheck_path, "-j", uri], stdout=PIPE) as proc:

        end_test_timestamp = str(datetime.now(tz=timezone.utc))

        shcheck_out = json.loads(proc.stdout.read())

        h_pres = list(shcheck_out[uri]['present'].keys())
        h_miss = shcheck_out[uri]['missing']
    
        output = {
            "scores": None,
            "notes": "Security headers present: " + str(len(h_pres)) + ". Missing: " + str(len(h_miss)),
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": shcheck_out
        }

        return output