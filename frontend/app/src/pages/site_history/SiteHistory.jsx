import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";


const SiteHistory = () => {
    const { site } = useParams()
    const [data, setData] = useState(null);         // data retrieved by the API call
    const [loading, setLoading] = useState(true);   // loading while fetch the API call

    useEffect(() => {
        fetchData();
    }, []);

    // API call
    const fetchData = async () => {
        try {
            const response = await fetch("http://localhost/api/v1/website/scores?url=https://www.comune.novellara.re.it/");
            const jsonData = await response.json();
            setData(jsonData);
            setLoading(false);
            
        } catch (error) {
            console.error("Error fetching data:", error);
            setLoading(false);
        }
    };

    return (
        <>
        { loading ? (
            <p>Loading component...</p>
        ) : (
            <h1>Storico {site}</h1>
        )}
      </>
    );
}

export default SiteHistory;