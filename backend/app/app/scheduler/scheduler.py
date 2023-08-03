import requests
from datetime import datetime, timedelta
import time

scheduled_tests = []

def main():
    """"""
    # chiamata API per ottenere tutti i crontab
    # conviene salvare localmente tutto e occasionalmente verificare se ce ne sono di nuovi
    # --> thread che ogni tot chiama API ?

    # First call
    while True:
        response = requests.get("http://backend/api/v1/schedule/get-all-active")
        if response.status_code == 200: break

    scheduled_tests = response.json()

    # Scheduler loop
    while True:
        for scheduled_test in scheduled_tests:
            # verifica ultima volta lanciato
            if canRun(scheduled_tests.last_time_launched):
                payload = {
                    "url": scheduled_test.url,
                    "test_types": [scheduled_test.test_type]
                }

                res = requests.post("http://backend/api/v1/website/run", json=payload)
        
        time.sleep(1)


    
def canRun(time, timedelta):
    if not time:
        return False
    
    # calcolare ogni quanto lanciare la run

    # verificare, rispetto ultima volta lanciato, se deve essere lanciato


if __name__ == "__main__":
    main()