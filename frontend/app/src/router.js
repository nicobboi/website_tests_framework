import { Routes, Route } from 'react-router-dom';
import Home from './pages/home/Home'

// Component that handles the frontend routing

const CustomRouter = () => {
    return (
        <>
            <Routes>

                {/* Routing list */}
                <Route path='/' element={<Home />} />

                {/* No match found handler */}
                <Route path='*' element={<Home />} />
            </Routes>
        </>
    );
}

export default CustomRouter;