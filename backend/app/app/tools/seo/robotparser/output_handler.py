from . import robotparser as rp 
from datetime import datetime, timezone

def get_output(url: str, robot_valid):
    output = {
        "scores": None,
        "notes": None,
        "start_test_timestamp": None,
        "end_test_timestamp": None,
        "json_report": None
    }

    if robot_valid:
        output["notes"] = "Robots.txt is valid!\n\n"
        output["start_test_timestamp"] = str(datetime.now(tz=timezone.utc))
        output["notes"] += rp.test(url)
        output["end_test_timestamp"] = str(datetime.now(tz=timezone.utc))
    else:
        output["notes"] = "Test not started because robots.txt is not valid!"

    return output