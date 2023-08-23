import { useParams } from "react-router-dom";
import useFetch from "react-fetch-hook";

import Chart from "../../components/site_history_chart/Chart";

const SiteHistory = () => {
    const { id } = useParams()

    const { isLoading, data, error } = useFetch("/api/v1/website/scores?website_id=" + id);
 
    if (error) {
        console.log(error)
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
          <>
            <div className="container">
              <h1 className="text-center">Storico <span className="text-muted h2 fst-italic">{data.url}</span></h1>
                <Chart url={data.url} reports_scores={data.reports_scores}/>
            </div>
          </>
        )}
      </>
    );
}

export default SiteHistory;