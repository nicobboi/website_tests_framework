from subprocess import Popen, PIPE
import json
import os
import inspect

# Runs all SECURITY tool tests and return a dict with all the desired output
def run_test(uri):
    output = {
        "sh-check": None,
        "ssllabs-scan": None
    }

    script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    
    # SHCHECK -------------------------------------------------------------------- #

    shcheck_path = script_dir + "/shcheck/shcheck.py"

    print("\'Security headers check\' test started.")
    with Popen([shcheck_path, "-j", uri], stdout=PIPE) as proc:
        shcheck_out = json.loads(proc.stdout.read())

        h_pres = list(shcheck_out[uri]['present'].keys())
        h_miss = shcheck_out[uri]['missing']
    
        output['sh-check'] = {
            "scores": None,
            "notes": "Security headers present: " + str(len(h_pres)) + ". Missing: " + str(len(h_miss)),
            "json_report": shcheck_out
        }

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #
    
    # SSLLABS-SCAN --------------------------------------------------------------- #

    ssllabs_path = script_dir + "/ssllabsscan/ssllabs-scan"

    print("\'SSLlabs-scan\' test started.")
    with Popen([ssllabs_path, "--verbosity", "error", uri], stdout=PIPE) as proc:
        ssllabs_scan_out = json.loads(proc.stdout.read())

        grade = ssllabs_scan_out[0]['endpoints'][0]['grade'][0] # to get the grade (without the "+" for the "A") 

        output['ssllabs-scan'] = {
            "scores": {
                "score_from_grade": score_from_grade(grade)
            },
            "notes": "SSL certificate's grade: " + grade,
            "json_report": ssllabs_scan_out[0]
        }

    print("Test ended.\n")
    # ----------------------------------------------------------------------------- #

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
