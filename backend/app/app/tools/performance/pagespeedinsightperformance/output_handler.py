from . import pagespeedperf as psp
from datetime import datetime, timezone

def get_output(url: str):
    start_test_timestamp = str(datetime.now(tz=timezone.utc))

    # run script for pagespeed insight test
    psp_out = psp.test(url)

    end_test_timestamp = str(datetime.now(tz=timezone.utc))

    try:
        # organize the output
        output = {
            "scores": {
                "performance_score":  int(psp_out['lighthouseResult']['categories']['performance']['score'] * 100),
            },
            "notes": "Loading speed: " + psp_out['loadingExperience']['overall_category'],
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": psp_out
        }
        
    except KeyError:
        print("Error on \'PageSpeed Insight (PERFORMANCE)\' test.\n")
        output = {
            "scores": None,
            "notes": "An error occured while testing this tool...",
            "start_test_timestamp": None,
            "end_test_timestamp": None,
            "json_report": None
        }

    return output