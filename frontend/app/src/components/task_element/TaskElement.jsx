import styles from "./taskelement.module.scss";

import dayjs from 'dayjs';
import utc from 'dayjs-plugin-utc';
dayjs.extend(utc);

const TaskElement = (props) => {
    const task = props.task;

    const statusColor = (status) => {
      switch (status) {
        case "SUCCESS": return "green";
        case "FAILURE": return "red";
        default: return "yellow";
      }
    }

    return (
      <>
        <div className="mt-3">
          <ul className={`${styles.list} list-inline`}>
            <li
              className={`d-flex justify-content-between ${styles.scheduleItem}`}
            >
              <div className="d-flex flex-row align-items-center">
                <div className="ms-4">
                  {/* URL */}
                  <h6 className="mb-0">
                    {task.test_type}
                  </h6>
                  <div
                    className={`d-flex flex-row mt-1 text-black-50 ${styles.dateTime}`}
                  >
                    <div className="mt-1">
                      {/* START TIME */}
                      <i className="fa-regular fa-calendar"></i>
                      <span className="ms-2">
                        {dayjs(task.finished_time)
                          .utcOffset(dayjs().utcOffset())
                          .format("DD/MM/YYYY HH:mm")}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="d-flex align-items-center me-5">
                <span style={ {color: statusColor(task.status)} }>{task.status}</span>
              </div>

            </li>
          </ul>
        </div>
      </>
    );
}

export default TaskElement;