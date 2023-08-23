import { Routes, Route } from 'react-router-dom';
import Home from './pages/home/Home';
import SiteHistory from './pages/site_history/SiteHistory';
import RunTest from './pages/run_test/RunTest';
import JobList from './pages/job_list/JobList';

// Component that handles the frontend routing

const CustomRouter = () => {
    return (
        <>
            <Routes>
                {/* Routing list */}
                <Route path='/' element={<Home />} /> 
                <Route path='/site-history/:id' element={<SiteHistory />} />
                <Route path='/run-test' element={<RunTest />} />
                <Route path='/job-list' element={<JobList />} /> 

                {/* No match found handler */}
                <Route path='*' element={<Home />} />
            </Routes>
        </>
    );
}

export default CustomRouter;