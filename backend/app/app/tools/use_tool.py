# Script to test tools's outputs and to print them

# global list to stores all reports which will be sent to db 
run_reports = []

def run_test(uri: str, test_type: str):
    #print("Testing \'" + uri + "\'.\n")

    tests = {
        "security":         securityTest,
        "performance":      performanceTest,
        "accessibility":    accessibilityTest,
        "seo":              SEOTest,
        "validation":       validationTest,
    }

    if test_type in tests.keys():
        tests[test_type](uri=uri)

    # if there are reports (call is valid), then push them into the db
    if run_reports:
        print("All tests ended.\n")
        pushToDB(uri)


# --- TESTS ----------------------------------------------------------------------------- #


# Runs the security tests (ssllabs-scan and shcheck) and prints the desired output
def securityTest(uri):
    from .security import securitytest

    print("Executing SECURITY test... \n")
    
    security_output = securitytest.run_test(uri)
    #print(security_output)

    addToReport("security", security_output)

    print("Security test ended.\n")


# Runs the performance test (PageSpeed Insight) and prints the desired output
# OUTPUT:
#   PageSpeed Insight: ...
def performanceTest(uri):
    from .performance import performancetest

    print("Executing PERFORMANCE test...\n")

    performance_output = performancetest.run_test(uri)
    #print(performance_output)

    addToReport("performance", performance_output)

    print("Performance test ended.\n")
    

# Runs the accessibility test (Mauve++) and prints the desired output
def accessibilityTest(uri):  
    from .accessibility import accessibilitytest

    print("Executing ACCESSIBILITY test.\n")

    accessibility_out = accessibilitytest.run_test(uri)
    #print(accessibility_out)

    addToReport("accessibility", accessibility_out)

    print("Accessibility test ended.\n")


# Runs the validation test (pa-website-validator) and prints the desired output
# OUTPUT:
#   pa-website-validator: ...
def validationTest(uri):
    from .validation import validationtest

    print("Executing VALIDATION test...\n")

    validation_out = validationtest.run_test(uri)
    #print(validation_out)

    addToReport("validation", validation_out)

    print("Validation test ended.\n")


# Runs the SEO tests and prints the output
def SEOTest(uri):
    from .seo import seotest

    print("Executing SEO test...\n")

    # returns a dict with key=test name and value=result of the test
    seo_output = seotest.run_test(uri)
    #print(seo_output)

    addToReport("seo", seo_output)

    print("SEO test ended.\n")


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
                print("Report sent.")
            else:
                print("Error sending report. Error: " + str(res.status_code))
        except requests.exceptions.ConnectionError:
            print("Connection error.\nShutting down...")
            exit(1)
        finally:
            session.close()

    run_reports.clear()

