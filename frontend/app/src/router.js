import { Routes, Route } from 'react-router-dom';
import Home from './pages/home/Home';
import SiteHistory from './pages/site_history/SiteHistory';
import ReportDetails from './pages/report_details/ReportDetails';
import RunTest from './pages/run_test/RunTest';

// Component that handles the frontend routing

const CustomRouter = () => {
    return (
        <>
            <Routes>
                {/* Routing list */}
                <Route path='/' element={<Home />} /> 
                <Route path='/site-history/:id' element={<SiteHistory />} />
                <Route path='/report/:id' element={<ReportDetails />}/>
                <Route path='/run-test' element={<RunTest />}/>

                {/* No match found handler */}
                <Route path='*' element={<Home />} />
            </Routes>
        </>
    );
}

export default CustomRouter;