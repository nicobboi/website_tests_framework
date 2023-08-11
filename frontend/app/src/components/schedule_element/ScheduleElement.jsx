import { useState } from "react";
import styles from "./scheduleelement.module.scss";

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

const ScheduleElement = (props) => {
    const schedule = props.schedule;

    // schedule info to send via API
    const initialTime = new Date(); initialTime.setHours(schedule.schedule_info.hour, schedule.schedule_info.min);
    const [scheduleTime, setScheduleTime] = useState(dayjs(initialTime));
    const [days, setDays] = useState(schedule.schedule_info.days);

    const [active, setActive] = useState(schedule.active);
    const [modified, setModified] = useState(false);

    // reset all changes not confirmed
    const resetStatus = () => {
        setScheduleTime(dayjs(new Date()))
        setDays([])

        setActive(schedule.active);
        setModified(false);
    }

    // commit the changes to database
    const commitChanges = () => {
      if (!modified) return;

      const payload = {
        min: scheduleTime.$m,
        hour: scheduleTime.$H,
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

    function formatDate(inputDateStr) {
      const inputDate = new Date(inputDateStr);
      
      const day = inputDate.getDate().toString().padStart(2, '0');
      const month = (inputDate.getMonth() + 1).toString().padStart(2, '0');
      const year = inputDate.getFullYear();
      
      const hours = inputDate.getHours().toString().padStart(2, '0');
      const minutes = inputDate.getMinutes().toString().padStart(2, '0');
      
      const formattedDate = `${day}/${month}/${year} ${hours}:${minutes}`;
      return formattedDate;
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
      setModified(true);
    };

    /* -------------------------------------------- */

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
                  <span className="ms-2">{schedule.last_time_launched ? formatDate(schedule.last_time_launched) : "Schedule not launched yet"}</span>
                </div>
                <div>
                  <i className="fa-solid fa-layer-group"></i>
                  <span className="ms-2 text-muted">~{schedule.n_run}</span>
                </div>
              </div>

              {/* crontab info */}
              <div className="d-flex flex-row mx-2">
                <TimePicker
                  className="me-2"
                  sx={{ width: 150 }}
                  label="Select schedule time"
                  value={scheduleTime}
                  onChange={(newValue) => {setScheduleTime(newValue); setModified(true);}}
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
                      <OutlinedInput id="select-multiple-chip" label="Chip" />
                    }
                    renderValue={(selected) => (
                      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
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