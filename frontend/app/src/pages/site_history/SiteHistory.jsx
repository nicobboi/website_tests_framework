import { useParams } from "react-router-dom";
import useFetch from "react-fetch-hook";

const SiteHistory = () => {
    const { id } = useParams()

    // const url = new URL('http://localhost/api/v1/website/scores?')
    
    const { isLoading, data, error } = useFetch("http://localhost/api/v1/website/scores?website_id=" + id);
 
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
        { isLoading ? (
            <p>Loading component...</p>
        ) : (
            <>
                <h1>Storico {data.url}</h1>
            </>
        )}
      </>
    );
}

export default SiteHistory;