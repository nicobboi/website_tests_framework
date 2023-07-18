
const Navbar = () => {
  return (
    <>
      <nav className="navbar navbar-light bg-light">

        <div className="container-fluid">
          <a className="navbar-brand">Progetto</a>
          <form className="d-flex">
            <input
              className="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button className="btn border" type="submit">
              Search
            </button>
          </form>
        </div>

      </nav>
    </>
  );
};

export default Navbar;