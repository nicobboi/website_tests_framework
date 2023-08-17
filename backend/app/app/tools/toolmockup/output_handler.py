import random
import lorem
import time
from datetime import datetime, timedelta, timezone

def get_output(url: str, min_score=0, max_score=100):
    time_now = datetime.now(timezone.utc)
    start_test_timestamp = random_date(str(time_now), str(time_now+timedelta(days=10)), random.random())

    # organize the output
    output = {
        "scores": {
            "mockup_score": random.randint(min_score, max_score),
        },
        "notes": lorem.paragraph(),
        "start_test_timestamp": str(start_test_timestamp),
        "end_test_timestamp": str(random_date(str(start_test_timestamp), str(start_test_timestamp+timedelta(minutes=10)), random.random())),
        "json_report": {
            "url": url,
            "data": {
                "sample-data-1": random.randint(0, 50),
                "sample-data-2": random.randint(35, 347)
            },
            "info": {
                "sample-info-1": lorem.sentence(),
                "sample-info-2": lorem.paragraph()
            }
        }
    }

    return output



def str_time_prop(start, end, time_format, prop):
    """
    Get a time at a proportion of a range of two formatted times.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return datetime.fromtimestamp(ptime, tz=timezone.utc)


def random_date(start, end, prop):
    """
    Generate a random date between two given
    """
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S.%f%z', prop)