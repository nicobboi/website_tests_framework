from . import robotparser as rp 
from datetime import datetime
from zoneinfo import ZoneInfo

def get_output(uri, robot_valid):
    output = {
        "scores": None,
        "notes": None,
        "start_test_timestamp": None,
        "end_test_timestamp": None,
        "json_report": None
    }

    if robot_valid:
        output["notes"] = "Robots.txt is valid!\n\n"
        output["start_test_timestamp"] = str(datetime.now(tz=ZoneInfo("Europe/Rome")))
        output["notes"] += rp.test(uri)
        output["end_test_timestamp"] = str(datetime.now(tz=ZoneInfo("Europe/Rome")))
    else:
        output["notes"] = "Test not started because robots.txt is not valid!"

    return output