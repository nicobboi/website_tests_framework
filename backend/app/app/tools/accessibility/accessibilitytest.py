# import here the output handlers
from ..toolmockup import output_handler as mockup
from .mauve import output_handler as mauve

def run_test(uri):
    # insert here the name of the tools used
    output = {
        "accessibility-mockup": None,
        # "mauve++": None
    }

    # MAUVE++ -------------------------------------------------------------------- #

    # print("\'Mauve++\' test started.")

    # output["mauve++"] = mauve.get_output(uri)

    # print("Test ended.\n")

    # MOCKUP --------------------------------------------------------------------- #

    print("\'Mockup\' test started.")

    output["accessibility-mockup"] = mockup.get_output(uri, min_score=55, max_score=78)

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output