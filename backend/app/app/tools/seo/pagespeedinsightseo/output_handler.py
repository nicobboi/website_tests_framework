from . import pagespeedseo as pss
from datetime import datetime, timezone

def get_output(url: str):
    start_test_timestamp = str(datetime.now(tz=timezone.utc))

    # runs pagespeed insight seo test
    pss_out = pss.test(url)

    end_test_timestamp = str(datetime.now(tz=timezone.utc))
    
    try:
        # organizing pss output 
        seo_score = int(pss_out["lighthouseResult"]["categories"]["seo"]["score"] * 100)
        # n_audits = len(pss_out["lighthouseResult"]["categories"]["seo"]["auditRefs"])

        # NEW OUTPUT (SQLite)
        output = {
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
        output = {
            "stats": None,
            "notes": {
                "info": "An error occured while testing this tool..."
            },
            "documents": None
        }

    return output, bool(pss_out["lighthouseResult"]["audits"]["robots-txt"]["score"])