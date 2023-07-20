import { useParams } from "react-router-dom";
import useFetch from "react-fetch-hook";

const RerportDetails = () => {
    const { id } = useParams()

    return (
        <>
            <h1>Dettagli report: "{id}"</h1>
        </>
    );
}

export default RerportDetails;