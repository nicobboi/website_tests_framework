from .pagespeedinsightseo import pagespeedseo as pss
from .robotparser import robotparser as rp 
from datetime import datetime
from zoneinfo import ZoneInfo

# Runs all SEO tool tests and return a dict with all the desired output
def run_test(uri):
    # tools's output returned
    output = {
        "pagespeed_seo": None,
        "robot_parser": None
    }

    # PAGESPEED INSIGHT SEO --------------------------------------------------------- #

    print("\'PageSpeed Insight SEO\' test started.")

    start_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))

    # runs pagespeed insight seo test
    pss_out = pss.test(uri)

    end_test_timestamp = str(datetime.now(tz=ZoneInfo("Europe/Rome")))
    
    try:
        # organizing pss output 
        seo_score = int(pss_out["lighthouseResult"]["categories"]["seo"]["score"] * 100)
        # n_audits = len(pss_out["lighthouseResult"]["categories"]["seo"]["auditRefs"])
        robot_valid = bool(pss_out["lighthouseResult"]["audits"]["robots-txt"]["score"])

        # NEW OUTPUT (SQLite)
        output['pagespeed_seo'] = {
            "scores": {
                "seo_score": seo_score,
            },
            "notes": None,
            "start_test_timestamp": start_test_timestamp,
            "end_test_timestamp": end_test_timestamp,
            "json_report": pss_out
        }

    except KeyError:
        print("Error on \'PageSpeed Insight (SEO)\' test.\n")
        output['pagespeed_seo'] = {
            "stats": None,
            "notes": {
                "info": "An error occured while testing this tool..."
            },
            "documents": None
        }

    print("Test ended\n")

    # ------------------------------------------------------------------------------- #

    # ROBOT PARSER ------------------------------------------------------------------ #    

    output["robot_parser"] = {
        "scores": None,
        "notes": None,
        "start_test_timestamp": None,
        "end_test_timestamp": None,
        "json_report": None
    }

    print("\'Robot parser\' test started.")
    if robot_valid:
        output["robot_parser"]["notes"] = "Robots.txt is valid!\n\n"
        output["robot_parser"]["start_test_timestamp"] = str(datetime.now(tz=ZoneInfo("Europe/Rome")))
        output["robot_parser"]["notes"] += rp.test(uri)
        output["robot_parser"]["end_test_timestamp"] = str(datetime.now(tz=ZoneInfo("Europe/Rome")))
    else:
        output["robot_parser"]["notes"] = "Test not started because robots.txt is not valid!"
    print("Test ended\n")

    # ------------------------------------------------------------------------------- #

    return output
