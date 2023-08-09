import useFetch from "react-fetch-hook";
import styles from "./scheduleslist.module.scss";

import ScheduleElement from "../../components/schedule_element/ScheduleElement";

const SchedulesList = () => {
    const { isLoading, data, error } = useFetch("http://localhost/api/v1/schedule/get-all");
  
    if (error) {
        console.log(error)
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

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

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
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
                    <div className={styles.icons}>
                      <i className="fa fa-search"></i>
                      <i className="fa fa-ellipsis-h"></i>
                    </div>
                  </div>

                  {/* ROWs */}
                  {data.map((schedule, index) => (
                    <ScheduleElement key={index} schedule={schedule} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </>
    );
}

export default SchedulesList;