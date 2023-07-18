import Table from "../../components/home_table/Table";
import { useEffect, useState } from "react";

const Home = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true); // 'true' default

    useEffect(() => {
        fetchData();
    }, []);

    // API call
    const fetchData = async () => {
        try {
            const response = await fetch("http://localhost/api/v1/website/average-scores");
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
            <Table table_data={data}/>
        )}
      </>
    );
}

export default Home;