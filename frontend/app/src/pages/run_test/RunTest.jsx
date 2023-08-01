import { useForm }  from  "react-hook-form";
import { useState } from "react";

const RunTest = () => {
    const { register, handleSubmit, formState:{errors} } = useForm();
    const [response, setResponse] = useState(null);
    const [testMode, setTestMode] = useState("run");

    const onSubmit = (data) => {
        const payload = {
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

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        };
        fetch("http://localhost/api/v1/website/run", requestOptions)
            .then(response => response.json()) 
            .then(json => {
                setResponse(json);
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
            className="
          form-floating row mt-3"
            onSubmit={handleSubmit(onSubmit)}
          >
            {/* URL and SUBMIT */}
            <div className="col-6 mb-3">
              <label htmlFor="url-input" className="form-label">
                URL
              </label>
              <input
                name="url"
                type="text"
                className="form-control"
                id="url-input"
                placeholder="https://site-name.domain"
                {...register("url", { required: true })}
              />
              {/* Error handling */}
              <span className="fs-6 text-danger">
                {errors.url && <p>This field is required!</p>}
              </span>

              {/* CRONTAB INFO */}
              {testMode === "schedule" && (
                <>
                  <div className="mt-2">Crontab Info</div>
                  <div className="d-flex flex-row justify-content-evenly">
                    <div className="input-group input-group-sm mt-1 mx-1">
                      <div className="d-flex flex-column align-items-center align-items-center">
                        <label htmlFor="minutes" style={{"font-size": 12}} className="form-label mx-1">
                          Minutes
                        </label>
                        <input
                          type="text"
                          className="form-control mx-1"
                          id="minutes"
                          placeholder="0-59"
                        />
                      </div>
                    </div>
                    <div className="input-group input-group-sm mt-1 mx-1">
                      <div className="d-flex flex-column align-items-center">
                        <label htmlFor="hours" style={{"font-size": 12}} className="form-label mx-1">
                          Hours
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="0-23"
                        />
                      </div>
                    </div>
                    <div className="input-group input-group-sm mt-1 mx-1">
                      <div className="d-flex flex-column align-items-center">
                        <label htmlFor="days-of-week" style={{"font-size": 12}} className="form-label mx-1">
                          Days week
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="0-6"
                        />
                      </div>
                    </div>
                    <div className="input-group input-group-sm mt-1 mx-1">
                      <div className="d-flex flex-column align-items-center">
                        <label htmlFor="Days-of-months" style={{"font-size": 12}} className="form-label mx-1">
                          Days month
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="1-31"
                        />
                      </div>
                    </div>
                    <div className="input-group input-group-sm mt-1 mx-1">
                      <div className="d-flex flex-column align-items-center">
                        <label htmlFor="Months-of-year" style={{"font-size": 12}} className="form-label mx-1">
                          Months year
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="1-12"
                        />
                      </div>
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