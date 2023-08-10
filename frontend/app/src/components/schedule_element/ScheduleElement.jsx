import { useState } from "react";
import styles from "./scheduleelement.module.scss";

const ScheduleElement = (props) => {
    const schedule = props.schedule;

    const [mins, setMins] = useState(schedule.schedule_info.min);
    const [hours, setHours] = useState(schedule.schedule_info.hour);
    const [days, setDays] = useState(schedule.schedule_info.day);
    // const [weeks, setWeeks] = useState(schedule.crontab.week);
    // const [months, setMonths] = useState(schedule.crontab.month);

    const [active, setActive] = useState(schedule.active);
    const [modified, setModified] = useState(false);

    // reset all changes not confirmed
    const resetStatus = () => {
        setMins(schedule.schedule_info.min);
        setHours(schedule.schedule_info.hour);
        setDays(schedule.schedule_info.day);
        // setWeeks(schedule.crontab.week);
        // setMonths(schedule.crontab.month);

        setActive(schedule.active);
        setModified(false);
    }

    // commit the changes to database
    const commitChanges = () => {
      const payload = {
        min: mins,
        hour: hours,
        day: days,
        active: active,
        last_time_launched: null
      }

      const request_url = "http://localhost/api/v1/schedule/update?schedule_id=" + schedule.id;

      // API call to change schedule info
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      };
      fetch(request_url, requestOptions)
          .then(response => response.json()) 
          .then(json => {
              setTimeout(() => 3000);
          })
          .catch(err => console.log("Error sending data: ", err));

      setModified(false);
    }

    // delete the schedule
    const deleteSchedule = () => {
      // check if the use is sure

      const request_url = "http://localhost/api/v1/schedule/remove?schedule_id=" + schedule.id;

      // API call to change schedule info
      fetch(request_url, {method: 'POST'})
          .then(response => response.json()) 
          .then(json => {
              setTimeout(() => 3000);
          })
          .catch(err => console.log("Error sending data: ", err));

      // delete this child component
      props.ondelete(props.url, props.data_index);
    }

    return (
      <>
        <div className="mt-3">
          <ul className={`${styles.list} list-inline`}>
            <li
              className={`d-flex justify-content-between ${styles.scheduleItem}`}
            >
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
                      ? ` fa-check-circle ${styles.checkicon}`
                      : ` fa-xmark-circle ${styles.xmarkicon}`)
                  }
                ></i>

                <div className="ms-4">
                  {/* URL */}
                  <h6 className="mb-0">
                    {schedule.test_type} {modified ? "*" : ""}
                  </h6>
                  <div
                    className={`d-flex flex-row mt-1 text-black-50 ${styles.dateTime}`}
                  >
                    <div className="mt-1">
                      {/* START TIME */}
                      <i className="fa-regular fa-calendar"></i>
                      <span className="ms-2">{schedule.scheduled_time}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* last time + run times */}
              <div className="d-flex flex-column mt-2">
                <div className="date-time">
                  <i className="fa-regular fa-clock"></i>
                  <i className="fa-solid fa-backward ms-1"></i>
                  <span className="ms-2">{schedule.last_time_launched}</span>
                </div>
                <div>
                  <i className="fa-solid fa-layer-group"></i>
                  <span className="ms-2 text-muted">~{schedule.n_run}</span>
                </div>
              </div>

              {/* crontab info */}
              <div className="d-flex flex-row mx-5">
                <div className="form-floating">
                  <input
                    type="text"
                    id="minutes"
                    className="form-control schedule-info-box mx-1"
                    value={mins}
                    onChange={(event) => {
                      setMins(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label htmlFor="minutes">minutes</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="hours"
                    className="form-control schedule-info-box mx-1"
                    value={hours}
                    onChange={(event) => {
                      setHours(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label htmlFor="hours">hours</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="days"
                    className="form-control schedule-info-box mx-1"
                    value={days}
                    onChange={(event) => {
                      setDays(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label htmlFor="days">days</label>
                </div>
                {/* <div className="form-floating">
                  <input
                    type="text"
                    id="months"
                    className="form-control schedule-info-box mx-1"
                    value={weeks}
                    onChange={(event) => {
                      setWeeks(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label htmlFor="months">months</label>
                </div>
                <div className="form-floating">
                  <input
                    type="text"
                    id="years"
                    className="form-control schedule-info-box mx-1"
                    value={months}
                    onChange={(event) => {
                      setMonths(event.target.value);
                      setModified(true);
                    }}
                  />
                  <label htmlFor="years">years</label>
                </div> */}
              </div>
              <div className={`${styles.cDropdown} my-auto`}>
                <button className={`btn ${styles.scheduleInfoBtn} p-3`}>
                  <i className="fa-solid fa-ellipsis-vertical my-auto fs-5"></i>
                </button>
                <ul className={`${styles.cDropdownContent} list-unstyled`}>
                  <li onClick={() => commitChanges()}>Commit changes</li>
                  <li onClick={() => resetStatus()}>Reset</li>
                  <li onClick={() => deleteSchedule()}>Delete</li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </>
    );
}

export default ScheduleElement;