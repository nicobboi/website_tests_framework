import { useParams } from "react-router-dom";


const SiteHistory = () => {
    const { site } = useParams()

    return (
        <>
            <h1>Storico {site}</h1>
        </>
    );
}

export default SiteHistory;