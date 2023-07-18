import { Routes, Route } from 'react-router-dom';
import Home from './pages/home/Home'
import SiteHistory from './pages/site_history/SiteHistory'

// Component that handles the frontend routing

const CustomRouter = () => {
    return (
        <>
            <Routes>
                {/* Routing list */}
                <Route path='/' element={<Home />} /> 
                <Route path='/sitehistory/:site' element={<SiteHistory />} />

                {/* No match found handler */}
                <Route path='*' element={<Home />} />
            </Routes>
        </>
    );
}

export default CustomRouter;