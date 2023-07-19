import Table from "../../components/home_table/Table";
import useFetch from "react-fetch-hook";

const Home = () => {
    const { isLoading, data, error } = useFetch("http://localhost/api/v1/website/latest-scores");
 
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
            <Table table_data={data}/>
        )}
      </>
    );
}

export default Home;