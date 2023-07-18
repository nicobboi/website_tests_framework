// import here the layout components
import Navbar from './Navbar'

const Layout = ({children}) => {
    return (
        <>
            <Navbar />
            <main className='container-fluid pt-2'>{children}</main>
            {/* Footer */}
        </>
    );
}

export default Layout;