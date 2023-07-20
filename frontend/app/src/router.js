import { Routes, Route } from 'react-router-dom';
import Home from './pages/home/Home'
import SiteHistory from './pages/site_history/SiteHistory'
import ReportDetails from './pages/report_details/ReportDetails';

// Component that handles the frontend routing

const CustomRouter = () => {
    return (
        <>
            <Routes>
                {/* Routing list */}
                <Route path='/' element={<Home />} /> 
                <Route path='/site-history/:id' element={<SiteHistory />} />
                <Route path='/report/:id' element={<ReportDetails />}/>

                {/* No match found handler */}
                <Route path='*' element={<Home />} />
            </Routes>
        </>
    );
}

export default CustomRouter;