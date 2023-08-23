import useFetch from "react-fetch-hook";

import dayjs from 'dayjs';
import utc from 'dayjs-plugin-utc';
dayjs.extend(utc);

const ReportDetails = (props) => {
    // API call
    const { isLoading, data, error } = useFetch("/api/v1/report/get?id=" + props.report_id);
 
    if (error) {
        console.log(error)
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

    // handler download JSON report
    const downloadFile = () => {
        const jsonData = JSON.stringify(data.json_report);

        const blob = new Blob([jsonData], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'report.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // handle change report details
    const changeReport = (event) => {
      if (event.target.title === "Previous report") {
        props.change_details(props.report_index-1, props.dataset_index);
      } else if (event.target.title === "Next report"){
        props.change_details(props.report_index+1, props.dataset_index);
      }
    }

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
          <>
            <div className="container">
              <h1 className="text-center">{data.tool.name} | n. {props.report_index+1}</h1>
              <div className="row mt-5">
                <div className="col-6">
                  URL: <span className="text-muted">{data.url}</span>
                  <br />
                  Test type: <span>{data.tool.type}</span>
                  <br />
                  Test ended at:{" "}
                  <span className="text-muted">{dayjs(data.end_test_time).utcOffset(dayjs().utcOffset()).format('DD/MM/YYYY HH:mm')}</span>
                  <br />
                  Test duration time: <span>{data.test_duration_time}</span>
                </div>
                <div className="col-6">
                  Notes: <br /> <span className="text-muted">{data.notes}</span>
                </div>
              </div>
              <div className="row mt-3">
                SCORES: <br />
                <div>
                  {data.scores.map((score, index) => (
                    <div key={index}>
                      {score.name}: {score.score} <br />
                    </div>
                  ))}
                </div>
              </div>
              <div className="row mt-3">
                Download full report:
                <div>
                  JSON:{" "}
                  <button
                    className="btn border border-dark ms-2"
                    onClick={downloadFile}
                  >
                    Download
                  </button>
                </div>
              </div>
              <div className="row mt-3">
                <div className="col-6" onClick={changeReport}>
                  <button className="btn p-3 text-start" title="Previous report">
                    <i className="fa-solid fa-arrow-left fs-3" title="Previous report"></i>
                  </button>
                </div>
                <div className="col-6 text-end" onClick={changeReport}>
                  <button className="btn p-3" title="Next report">
                    <i className="fa-solid fa-arrow-right fs-3" title="Next report"></i>
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </>
    );
}

export default ReportDetails;