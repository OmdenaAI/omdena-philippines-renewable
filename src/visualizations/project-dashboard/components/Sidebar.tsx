const Sidebar = () => {
  return (
    <>
      <div className="sidebar">
        <div className="sidebar-navigation">
          <div className="top-bar">
            <img src="/images/omdena-ph.png" />
            <div className="mt-1 mr-2 d-flex">
              <input
                type="text"
                placeholder="Search Places.."
                className="form-control"
                id="search-input"
              />
              <button className="btn btn-default ml-2">
                <i className="la la-search" />
              </button>
            </div>
          </div>
          <div className="nav-links">
            <span className="active">DATASET</span>
            <span>NOTEBOOKS</span>
            <span>About</span>
          </div>
        </div>

        <div className="sidebar-content">
          <div className="card p-2">
            <p>Sample Card</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
