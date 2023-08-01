import { useParams } from "react-router-dom";
import useFetch from "react-fetch-hook";

const ReportDetails = () => {
    const { id } = useParams()

    // API call
    const { isLoading, data, error } = useFetch("http://localhost/api/v1/report/get?id=" + id);
 
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

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
          <>
            <div className="container">
              <h1 className="text-center">Dettagli report: {data.tool.name}</h1>
              <div className="row mt-3">
                <div className="col-6">
                  URL: <span className="text-muted">{data.url}</span>
                  <br />
                  Test type: <span>{data.tool.type}</span>
                  <br />
                  Test ended at:{" "}
                  <span className="text-muted">{data.end_test_time}</span>
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
                  {data.scores.map((score) => (
                    <>
                      {score.name}: {score.score} <br />
                    </>
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
                <div className="col-6">
                  <button className="btn p-3 text-start" title="Previous report">
                    <i className="fa-solid fa-arrow-left fs-3"></i>
                  </button>
                </div>
                <div className="col-6 text-end">
                  <button className="btn p-3">
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