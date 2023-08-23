import ReportRow from "./ReportRow";
import useFetch from "react-fetch-hook";

const ReportTypeDetails = (props) => {
    const { isLoading, data, error } = useFetch("/api/v1/report/get-all-filtered?url=" + props.reports_url + "&type=" + props.reports_type);
 
    if (error) {
        console.log(error)
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

    console.log(data);

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
          <div className="container">
            <div className="table-responsive">
              <table className="table table-sm border-black">
                <thead>
                  <tr>
                    <th scope="col">n.</th>
                    <th scope="col">Tool</th>
                    <th scope="col">Scores</th>
                    <th scope="col">End time</th>
                    <th scope="col">Notes</th>
                  </tr>
                </thead>
                {
                  data.map((element, index) => (
                    <ReportRow 
                      key={index}
                      id={index+1}
                      tool={element.tool.name}
                      scores={element.scores}
                      end_time={element.end_test_time}
                      notes={element.notes}
                    />
                  ))
                }
              </table>
            </div>
          </div>
        )}
      </>
    );
}

export default ReportTypeDetails;