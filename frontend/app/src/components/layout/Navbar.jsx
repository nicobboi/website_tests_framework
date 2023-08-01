import { Link } from "react-router-dom";

const Navbar = () => {


  return (
    <>
      <nav className="navbar navbar-light navbar-expand-lg bg-light">
        <div className="container-fluid">
          <Link to="/" className="navbar-brand ms-4 fs-4">
            SITE TESTING
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-4">
              <li className="nav-item">
                <Link className="nav-link active" to="/run-test">
                  Start Test
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="#">
                  Scheduled test
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;