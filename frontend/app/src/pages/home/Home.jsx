import Table from "../../components/home_table/Table";
import { useEffect, useState } from "react";

const Home = () => {
    const [data, setData] = useState([
        {
            'site': 'https://www.comune.novellara.re.it/',
            'scores': {
                'accessibility': 34,
                'performance': 97,
                'security': 75,
                'seo': null,
                'validation': 93
            }
        },
        {
            'site': 'https://www.comunefinale.net/it-it/home',
            'scores': {
                'accessibility': 67,
                'performance': 89,
                'security': 90,
                'seo': 78,
                'validation': 56
            }
        }
    ]);
    const [loading, setLoading] = useState(false); // 'true' default

    useEffect(() => {
        //fetchData();
    }, []);

    // API call
    const fetchData = async () => {
        try {
            const response = await fetch("https://api.example.com/data");
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