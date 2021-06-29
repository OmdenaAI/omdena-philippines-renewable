const DetailsScreen = (props: any) => {
  return (
    <>
      <div className="details-screen fade-in">
        <div className="top-bar">
          <button
            className="btn btn-default fade-in"
            onClick={() => {
              props.setScreen("home");
            }}
          >
            <i className="la la-arrow-circle-left" />
          </button>
        </div>
        <div className="sidebar-content">{props.children}</div>
      </div>
    </>
  );
};

export default DetailsScreen;
