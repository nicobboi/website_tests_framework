from subprocess import Popen, PIPE
from datetime import datetime, timezone
import json
import os

def get_output(url: str):
    ssllabs_path = os.path.dirname(__file__) + "/ssllabs-scan"

    start_test_timestamp = str(datetime.now(tz=timezone.utc))

    with Popen([ssllabs_path, "--verbosity", "error", url], stdout=PIPE) as proc:
        ssllabs_scan_out = json.loads(proc.stdout.read())

        end_test_timestamp = str(datetime.now(tz=timezone.utc))

        grade = ssllabs_scan_out[0]['endpoints'][0]['grade'][0] # to get the grade (without the "+" for the "A") 

        output = {
            "scores": {
                "score_from_grade": score_from_grade(grade)
            },
            "notes": "SSL certificate's grade: " + grade,
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": ssllabs_scan_out[0]
        }

        return output

# returns the corresponding score from the given grade
def score_from_grade(grade):
    score = 0
    grades = {
        'A': 100,
        'B': 80,
        'C': 65,
        'D': 50,
        'E': 35,
        'F': 0
    }
    
    if grade in grades:
        score = grades[grade]
            
    return score