import { useForm }  from  "react-hook-form";
import { useState } from "react";

import { useNavigate, createSearchParams } from "react-router-dom";

import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import dayjs from 'dayjs';
import utc from 'dayjs-plugin-utc';
dayjs.extend(utc);

const RunTest = () => {
    const { register, handleSubmit, formState:{errors} } = useForm();
    const [response, setResponse] = useState(null);
    const [testMode, setTestMode] = useState("task");

    // schedule info to send via API
    const [scheduleTime, setScheduleTime] = useState(dayjs(new Date()));
    const [days, setDays] = useState([]);

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

        if (testMode === "task") {
          request_url = "/api/v1/website/run"
        } else if (testMode === "schedule") {
          payload = {
            time_info: scheduleTime.utcOffset(0).format('HH:mm:ssZ'),
            days: days,
            ...payload
          }
        
          request_url = "/api/v1/schedule/add"
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
                setResponse(json);
            })
            .catch(err => console.log("Error sending data: ", err));
    }

    const navigate = useNavigate()
    const toJobList = (url, test_mode) => {
      const params = { job: test_mode, url: url  }
      navigate({
        pathname: '/job-list/',
        search: `?${createSearchParams(params)}`
      })
    }

    /* SELECT COMPONENT CONF ---------------------- */
    const ITEM_HEIGHT = 48;
    const ITEM_PADDING_TOP = 8;
    const MenuProps = {
      PaperProps: {
        style: {
          maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
          width: 250,
        },
      },
    };

    const selectDays = [
      "monday",
      "tuesday",
      "wednesday",
      "thursday",
      "friday",
      "saturday",
      "sunday"
    ]

    function getStyles(day, days, theme) {
      return {
        fontWeight:
          days.indexOf(day) === -1
            ? theme.typography.fontWeightRegular
            : theme.typography.fontWeightMedium,
      };
    }
    const theme = useTheme();
    const handleChange = (event) => {
      const {
        target: { value },
      } = event;
      setDays(
        // On autofill we get a stringified value.
        typeof value === 'string' ? value.split(',') : value,
      );
    };

    /* -------------------------------------------- */

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

                    <TimePicker
                      sx={{ width: 150 }}
                      label="Select schedule time"
                      value={scheduleTime}
                      onChange={(newValue) => setScheduleTime(newValue)}
                    />
                    <FormControl sx={{ width: 250 }}>
                      <InputLabel id="demo-multiple-chip-label">
                        Select schedule days
                      </InputLabel>
                      <Select
                        labelId="demo-multiple-chip-label"
                        id="demo-multiple-chip"
                        multiple
                        value={days}
                        onChange={handleChange}
                        input={
                          <OutlinedInput
                            id="select-multiple-chip"
                            label="Chip"
                          />
                        }
                        renderValue={(selected) => (
                          <Box
                            sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}
                          >
                            {selected.map((value) => (
                              <Chip key={value} label={value} />
                            ))}
                          </Box>
                        )}
                        MenuProps={MenuProps}
                      >
                        {selectDays.map((day) => (
                          <MenuItem
                            key={day}
                            value={day}
                            style={getStyles(day, days, theme)}
                          >
                            {day}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </div>
                </>
              )}

              {/* TEST MODE (task / schedule) */}
              <div className="form-check mt-3">
                <input
                  className="form-check-input"
                  type="radio"
                  name="test-mode"
                  id="task-radio"
                  value="task"
                  checked={testMode === "task"}
                  onChange={(event) => {setTestMode(event.target.value); setResponse(null);}}
                />
                <label className="form-check-label" htmlFor="task-radio">
                  Single task test
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
                  onChange={(event) => {setTestMode(event.target.value); setResponse(null);}}
                />
                <label className="form-check-label" htmlFor="schedule-radio">
                  Schedule test
                </label>
              </div>

              <button className="btn btn-warning mt-3" type="submit">
                {testMode === "task" ? <>Launch Test</> : <>Schedule Test</>}
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
              {response ? (
                <>
                  <span>Tasks { testMode === "schedule" ? `scheduled` : `ran` } correctly!</span>
                  <br />
                  <button
                    className="btn"
                    onClick={() => toJobList(response[0].url, testMode)}
                  >
                    Check in { testMode } list
                  </button>
                </>
              ) : null}
            </span>
          </div>
        </div>
      </>
    );
}

export default RunTest;