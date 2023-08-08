import useFetch from "react-fetch-hook";
import "./scheduleslist.scss";

import ScheduleElement from "../../components/schedule_element/ScheduleElement";

const SchedulesList = () => {
    // get the current time in a formatted string like "dd/MM/YY hh:mm"
    const getCurrentDateFormatted = () => {
        const date = new Date();

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        const formattedString = `${day}/${month}/${year} ${hours}:${minutes}`;
        return formattedString;
    }
    
    // Schedule samples
    const schedule_1 = {
        url: "http://site1.domain",
        start_time: getCurrentDateFormatted(),
        last_time: getCurrentDateFormatted(),
        crontab: {
            min: "*",
            hour: "*",
            day: "*",
            week: "*",
            month: "*",
        },
        times_run: 50,
        active: true
    }
    const schedule_2 = {
        url: "http://site2.domain",
        start_time: getCurrentDateFormatted(),
        last_time: getCurrentDateFormatted(),
        crontab: {
            min: "*",
            hour: "*",
            day: "*",
            week: "*",
            month: "*",
        },
        times_run: 74,
        active: false
    }

    return (
      <>
        <div className="container">
          <h2 className="text-center mt-2">Schedules list</h2>

          <div className="container mt-3">
            <div className="row">
              <div className="col-md-12">
                <div className="d-flex justify-content-between align-items-center activity">
                  <div>
                    <i className="fa-regular fa-clock"></i>
                    <span className="ms-2">{getCurrentDateFormatted()}</span>
                  </div>
                  <div className="icons">
                    <i className="fa fa-search"></i>
                    <i className="fa fa-ellipsis-h"></i>
                  </div>
                </div>

                {/* ROWs */}
                <ScheduleElement schedule={schedule_1} />
                <ScheduleElement schedule={schedule_2} />

              </div>
            </div>
          </div>
        </div>
      </>
    );
}

export default SchedulesList;