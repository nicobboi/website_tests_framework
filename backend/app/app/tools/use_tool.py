from typing import List

# Script to test tools's outputs and to print them

# global list to stores all reports which will be sent to db 
run_reports = []

def run_tests(uri: str, test_type: List[str]):
    tests = {
        "SECURITY":         securityTest,
        "PERFORMANCE":      performanceTest,
        "ACCESSIBILITY":    accessibilityTest,
        "SEO":              SEOTest,
        "VALIDATION":       validationTest,
    }

    # if is present 'ALL', then test on all test types
    if "ALL" in test_type:
        for test in tests.values():
            test(uri)
    # else, test on types given by client
    else:
        for test_name in test_type:
            if not test_name in tests.keys():
                 continue
            tests[test_name](uri)

    # if there are reports (call is valid), then push them into the db
    if run_reports:
        pushToDB(uri)


# ALL TEST OUTPUT ARE DICT (use keys() to check the tools used for that output)

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
#   PageSpeed Insight: performance score, number of audits, ... (TODO: add more)
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
#   pa-website-validator: model compliace score, reccomandations tests score, ... (TODO: add more)
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


# TEST FUNCTION to send data into the db 
def Test(uri):
    print("Test API!\n")

    output = {
        "test_tool6": {
            'scores': {
                'score_1': 89, 
                'score_2': 13
            },
            'notes': "Stringhe con note.",
            'json_report': None
        } 
    }

    addToReport("test_type", output)



# add the report in the global list of reports
def addToReport(type, output):
    for tool in output:
        out = output[tool]

        report = {
            'notes': out['notes'],
            'json_report': out['json_report'],
            'tool': {
                'name': tool,
                'type': type,
            },
            'scores': [[{
                'name': name,
                'score': score
            } for name, score in out['scores'].items()], None][out['scores'] == None]
        }

        run_reports.append(report)

# Push a test result into the databa se using the custom API
def pushToDB(url):
    import requests
    from datetime import datetime

    for report in run_reports:
        payload = {
            'notes': report['notes'],
            'json_report': report['json_report'],
            'timestamp': str(datetime.now()),
            'tool': report['tool'],
            'scores': report['scores'],
            'url': url
        }

        try:
            # api request to send report's data into the database
            res = requests.post("http://localhost/api/v1/report/set", json=payload)
            if res.status_code == 200:
                print("Report \'" + report['tool'] +"\' sent.")
            else:
                print("Error sending report \'" + report['tool'] +"\'. Response: " + str(res.status_code) + ".")
        except requests.exceptions.ConnectionError:
            print("Connection error.\nShutting down...")
            exit(1)

    #print("\nAll report sent.\n")
    run_reports.clear()

