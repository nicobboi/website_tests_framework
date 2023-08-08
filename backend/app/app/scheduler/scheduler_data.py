import requests

def get_active_schedules():
    res_code = 422
    tries = 1
    print("[INFO]: Starting scheduler...")
    while res_code != 200 and tries <= 50:
        response = requests.get("http://backend/api/v1/schedule/get-all-active")
        res_code = response.status_code
        print("[INFO]: Request schedules (call n. " + str(tries) + "). Response: " + str(res_code) + ".")

    return response.json()
