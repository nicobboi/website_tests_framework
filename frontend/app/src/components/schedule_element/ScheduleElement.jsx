import { useState } from "react";
import "./scheduleelement.scss";

const ScheduleElement = (props) => {
    const schedule = props.schedule;

    const [mins, setMins] = useState(schedule.crontab.min);
    const [hours, setHours] = useState(schedule.crontab.hour);
    const [days, setDays] = useState(schedule.crontab.day);
    const [weeks, setWeeks] = useState(schedule.crontab.week);
    const [months, setMonths] = useState(schedule.crontab.month);

    const [active, setActive] = useState(schedule.active);
    const [modified, setModified] = useState(false);

    // reset all changes not confirmed
    const resetStatus = () => {
        setMins(schedule.crontab.min);
        setHours(schedule.crontab.hour);
        setDays(schedule.crontab.day);
        setWeeks(schedule.crontab.week);
        setMonths(schedule.crontab.month);

        setActive(schedule.active);
        setModified(false);
    }

    const commitChanges = () => {
        // API call to change schedule info

        setModified(false);
    }

    const deleteSchedule = () => {
        // check if the use is sure

        // API call to delete this schedule
    }

    return (
      <>
        <div className="mt-3">
          <ul className="list list-inline">
            <li className="d-flex justify-content-between schedule-item">
              <div className="d-flex flex-row align-items-center">
                {/* Is active icon */}
                <i
                  onClick={(event) => {
                    setActive(!active);
                    setModified(true);
                  }}
                  className={
                    "ms-3 fa " +
                    (active
                      ? " fa-check-circle checkicon"
                      : " fa-xmark-circle xmarkicon")
                  }
                ></i>

                <div className="ms-4">
                  {/* URL */}
                  <h6 className="mb-0">
                    {schedule.url} {modified ? "*" : ""}
                  </h6>
                  <div className="d-flex flex-row mt-1 text-black-50 date-time">
                    <div className="mt-1">
                      {/* START TIME */}
                      <i className="fa-regular fa-calendar"></i>
                      <span className="ms-2">{schedule.start_time}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* last time + run times */}
              <div className="d-flex flex-column mt-2">
                <div className="date-time">
                  <i class="fa-regular fa-clock"></i>
                  <i class="fa-solid fa-backward ms-1"></i>
                  <span className="ms-2">{schedule.last_time}</span>
                </div>
                <div>
                  <i class="fa-solid fa-layer-group"></i>
                  <span className="ms-2 text-muted">~{schedule.times_run}</span>
                </div>
              </div>

              {/* crontab info */}
              <div className="d-flex flex-row mx-5">
                <div className="form-floating">
                  <input
                    type="text"
                    id="minutes"
                    className="form-control crontab-box mx-1"
                    value={mins}
                    onChange={(event) => {
                      setMins(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label for="minutes">minutes</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="hours"
                    className="form-control crontab-box mx-1"
                    value={hours}
                    onChange={(event) => {
                      setHours(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label for="hours">hours</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="days"
                    className="form-control crontab-box mx-1"
                    value={days}
                    onChange={(event) => {
                      setDays(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label for="days">days</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="months"
                    className="form-control crontab-box mx-1"
                    value={weeks}
                    onChange={(event) => {
                      setWeeks(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label for="months">months</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="years"
                    className="form-control crontab-box mx-1"
                    value={months}
                    onChange={(event) => {
                      setMonths(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label for="years">years</label>
                </div>
              </div>
              <div className="c-dropdown my-auto">
                <button className="btn schedule-info-btn p-3">
                  <i className="fa-solid fa-ellipsis-vertical my-auto fs-5"></i>
                </button>
                <div className="c-dropdown-content">
                  <li onClick={() => commitChanges()}>Commit changes</li>
                  <li onClick={() => resetStatus()}>Reset</li>
                  <li onClick={() => deleteSchedule()}>Delete</li>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </>
    );
}

export default ScheduleElement;