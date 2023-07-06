from .pagespeedinsightperformance import pagespeedperf as psp

def run_test(uri):
    output = {
        "pagespeed_performance": None
    }

    # PAGESPEED INSIGHT PERFOMANCE ----------------------------------------------- #

    print("\'PageSpeed Insight PERFORMANCE\' test started.")

    # run script for pagespeed insight test
    psp_out = psp.test(uri)

    try:
        # organize the output
        output['pagespeed_performance'] = {
            "scores": {
                "performance_score":  int(psp_out['lighthouseResult']['categories']['performance']['score'] * 100),
            },
            "notes": "Loading speed: " + psp_out['loadingExperience']['overall_category'],
            "json_report": psp_out
        }
        
    except KeyError:
        print("Error on \'PageSpeed Insight (PERFORMANCE)\' test.\n")
        output['pagespeed_performance'] = {
            "stats": None,
            "notes": {
                "info": "An error occured while testing this tool..."
            },
            "documents": None
        }
            
    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output