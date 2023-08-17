import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Script to test tools's outputs and to print them

# global list to stores all reports which will be sent to db 
run_reports = []

def run_test(url: str, test_type: str):
    tests = {
        "security":         securityTest,
        "performance":      performanceTest,
        "accessibility":    accessibilityTest,
        "seo":              SEOTest,
        "validation":       validationTest,
    }

    if test_type in tests.keys():
        tests[test_type](url=url)

    # if there are reports (call is valid), then push them into the db
    if run_reports:
        logger.info("All tests ended.\n")
        pushToDB(url)


# --- TESTS ----------------------------------------------------------------------------- #


# Runs the security tests (ssllabs-scan and shcheck) and prints the desired output
def securityTest(url):
    from .security import securitytest

    logger.info("Executing SECURITY test... \n")
    
    security_output = securitytest.run_test(url)

    addToReport("security", security_output)

    logger.info("Security test ended.\n")


# Runs the performance test (PageSpeed Insight) and prints the desired output
def performanceTest(url):
    from .performance import performancetest

    logger.info("Executing PERFORMANCE test...\n")

    performance_output = performancetest.run_test(url)

    addToReport("performance", performance_output)

    logger.info("Performance test ended.\n")
    

# Runs the accessibility test (Mauve++) and prints the desired output
def accessibilityTest(url):  
    from .accessibility import accessibilitytest

    logger.info("Executing ACCESSIBILITY test.\n")

    accessibility_out = accessibilitytest.run_test(url)

    addToReport("accessibility", accessibility_out)

    logger.info("Accessibility test ended.\n")


# Runs the validation test (pa-website-validator) and prints the desired output
def validationTest(url):
    from .validation import validationtest

    logger.info("Executing VALIDATION test...\n")

    validation_out = validationtest.run_test(url)

    addToReport("validation", validation_out)

    logger.info("Validation test ended.\n")


# Runs the SEO tests and prints the output
def SEOTest(url):
    from .seo import seotest

    logger.info("Executing SEO test...\n")

    seo_output = seotest.run_test(url)

    addToReport("seo", seo_output)

    logger.info("SEO test ended.\n")


# add the report in the global list of reports
def addToReport(type, output):
    for tool in output:
        out = output[tool]

        report = {
            'tool': {
                'name': tool,
                'type': type,
            },
            'scores': None,
            'notes': out['notes'],
            'start_test_timestamp': out['start_test_timestamp'],
            'end_test_timestamp': out['end_test_timestamp'],
            'json_report': out['json_report'],
        }

        if out['scores']:
            report['scores'] = [{
                'name': name,
                'score': score
            } for name, score in out['scores'].items()]

        run_reports.append(report)

# Push a test result into the databa se using the custom API
def pushToDB(url):
    import requests

    session = requests.Session()
    session.trust_env = False

    for report in run_reports:
        payload = {
            "notes": report['notes'],
            "json_report": report['json_report'],
            "start_test_timestamp": report['start_test_timestamp'],
            "end_test_timestamp": report['end_test_timestamp'],
            "tool": report['tool'],
            "scores": report['scores'],
            "url": url
        }

        try:
            # api request to send report's data into the database
            api_url = "http://backend/api/v1/report/set"
            res = session.post(api_url, json=payload)
            if res.status_code == 200:
                logger.info("Report sent.")
            else:
                logger.warning("Error sending report. Error: " + str(res.status_code))
        except requests.exceptions.ConnectionError:
            logger.error("Connection error.\nShutting down...")
            exit(1)
        finally:
            session.close()

    run_reports.clear()

