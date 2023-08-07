import ReportRow from "./ReportRow";
import useFetch from "react-fetch-hook";

const ReportTypeDetails = (props) => {
    // const { isLoading, data, error } = useFetch("http://localhost/api/v1/");
 
    // if (error) {
    //     console.log(error)
    //     return (
    //     <div>
    //         <p>Code: {error.status}</p>
    //         <p>Message: {error.statusText}</p>
    //     </div>
    //     )
    // }

    return (
      <>
        <div className="container">
          <div className="table-responsive">
            <table className="table table-sm border-black">
              <thead>
                <tr>
                  <th scope="col">n.</th>
                  <th scope="col">Tool</th>
                  <th scope="col">End time</th>
                  <th scope="col">Notes</th>
                </tr>
              </thead>
              <ReportRow />
            </table>
          </div>
        </div>
      </>
    );
}

export default ReportTypeDetails;