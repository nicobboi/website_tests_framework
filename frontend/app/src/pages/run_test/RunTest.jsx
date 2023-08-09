import { useForm }  from  "react-hook-form";
import { useState } from "react";

const RunTest = () => {
    const { register, handleSubmit, formState:{errors} } = useForm();
    const [response, setResponse] = useState(null);
    const [testMode, setTestMode] = useState("run");

    const [mins, setMins] = useState(undefined);
    const [hours, setHours] = useState(undefined);
    const [days, setDays] = useState(undefined);

    // handle form submit
    const onSubmit = (data) => {
        var payload = {
            url: data["url"],
            test_types: []
        };

        if (data["accessibility-check"])
            payload["test_types"].push("accessibility");
        if (data["performance-check"])
            payload["test_types"].push("performance");
        if (data["security-check"])
            payload["test_types"].push("security");
        if (data["seo-check"])
            payload["test_types"].push("seo");
        if (data["validation-check"])
            payload["test_types"].push("validation");

        // console.log(payload);

        var request_url = ""

        if (testMode === "run") {
          request_url = "http://localhost/api/v1/website/run"
        } else if (testMode === "schedule") {
          payload = {
            min: data["minutes"],
            hour: data["hours"],
            day: data["days"],
            ...payload
          }
        
          request_url = "http://localhost/api/v1/schedule/add"
        }

        // API call to start a run/add a schedule
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        };
        fetch(request_url, requestOptions)
            .then(response => response.json()) 
            .then(json => {
                setResponse("Scheduled successfully!");
                setTimeout(() => setResponse(null), 3000);
            })
            .catch(err => console.log("Error sending data: ", err));
    }

    return (
      <>
        <div className="container">
          <h1 className="ms-3">Start Test</h1>

          {/* FORM */}
          <form
            className="form-floating row mt-4"
            onSubmit={handleSubmit(onSubmit)}
          >
            {/* URL and SUBMIT */}
            <div className="col-6 mb-3">
              <div className="input-group">
                <span className="input-group-text" id="icon-text-input">
                  <i className="fa-solid fa-globe"></i>
                </span>
                <input
                  name="url"
                  type="text"
                  className="form-control"
                  id="url-input"
                  placeholder="https://site-name.domain"
                  {...register("url", { required: true })}
                />
              </div>
              {/* Error handling */}
              <span className="fs-6 text-danger">
                {errors.url && <p>This field is required!</p>}
              </span>

              {/* SCHEDULE INFO */}
              {testMode === "schedule" && (
                <>
                  <div className="d-flex flex-row justify-content-evenly mt-3">
                    <div className="my-auto fs-3">
                      <i className="fa-regular fa-calendar-days"></i>
                    </div>
                    <div className="form-floating">
                      <input
                        type="number"
                        id="minutes"
                        className="form-control schedule-info-box mx-1"
                        value={mins}
                        onChange={(event) => {
                          console.log(event.target);
                          setMins(event.target.value);
                        }}
                        {...register("minutes")}
                      />
                      <label htmlFor="minutes">minutes</label>
                    </div>
                    <div className="form-floating">
                      <input
                        type="number"
                        id="hours"
                        className="form-control schedule-info-box mx-1"
                        value={hours}
                        onChange={(event) => {
                          setHours(event.target.value);
                        }}
                        {...register("hours")}
                      />
                      <label htmlFor="hours">hours</label>
                    </div>
                    <div className="form-floating">
                      <input
                        type="number"
                        id="days"
                        className="form-control schedule-info-box mx-1"
                        value={days}
                        onChange={(event) => {
                          setDays(event.target.value);
                        }}
                        {...register("days")}
                      />
                      <label htmlFor="days">days</label>
                    </div>
                  </div>
                </>
              )}

              {/* TEST MODE (run / schedule) */}
              <div className="form-check mt-3">
                <input
                  className="form-check-input"
                  type="radio"
                  name="test-mode"
                  id="run-radio"
                  value="run"
                  checked={testMode === "run"}
                  onChange={(event) => setTestMode(event.target.value)}
                />
                <label className="form-check-label" htmlFor="run-radio">
                  Single run test
                </label>
              </div>
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="radio"
                  name="test-mode"
                  id="schedule-radio"
                  value="schedule"
                  checked={testMode === "schedule"}
                  onChange={(event) => setTestMode(event.target.value)}
                />
                <label className="form-check-label" htmlFor="schedule-radio">
                  Schedule test
                </label>
              </div>

              <button className="btn btn-warning mt-3" type="submit">
                {testMode === "run" ? <>Launch Test</> : <>Schedule Test</>}
              </button>
            </div>

            <div className="col-6">
              {/* TEST TYPES */}
              <div className="ms-3">
                <div className="mb-2 fs-5">Choose test types:</div>
                <div className="mb-3">
                  <div className="form-check">
                    <input
                      name="test-types"
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="accessibility-check"
                      {...register("accessibility-check")}
                    />
                    <label
                      className="form-check-label"
                      htmlFor="accessibility-check"
                    >
                      Accessibility
                    </label>
                  </div>
                  <div className="form-check">
                    <input
                      name="test-types"
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="performance-check"
                      {...register("performance-check")}
                    />
                    <label
                      className="form-check-label"
                      htmlFor="performance-check"
                    >
                      Performance
                    </label>
                  </div>
                  <div className="form-check">
                    <input
                      name="test-types"
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="security-check"
                      {...register("security-check")}
                    />
                    <label
                      className="form-check-label"
                      htmlFor="security-check"
                    >
                      Security
                    </label>
                  </div>
                  <div className="form-check">
                    <input
                      name="test-types"
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="seo-check"
                      {...register("seo-check")}
                    />
                    <label className="form-check-label" htmlFor="seo-check">
                      SEO
                    </label>
                  </div>
                  <div className="form-check">
                    <input
                      name="test-types"
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="validation-check"
                      {...register("validation-check")}
                    />
                    <label
                      className="form-check-label"
                      htmlFor="validation-check"
                    >
                      Validation
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </form>

          <div className="row">
            <span className="fs-4 my-3 text-center text-success">
              {response}
            </span>
          </div>
        </div>
      </>
    );
}

export default RunTest;