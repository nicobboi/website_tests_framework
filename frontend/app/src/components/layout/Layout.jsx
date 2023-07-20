// import here the layout components
import Navbar from './Navbar'

const Layout = ({children}) => {
    return (
        <>
            <Navbar />
            <main className='container-fluid pt-2'>{children}</main>
            <footer>
                <ul className='nav justify-content-center bg-light py-2'>
                    <li className='nav-item'>
                        <a className='nav-link' href='/docs'>OpenApi</a>
                    </li>
                    <li className='nav-item'>
                        <a className='nav-link' href='/redoc'>ReDoc</a>
                    </li>
                </ul>
            </footer>
        </>
    );
}

export default Layout;