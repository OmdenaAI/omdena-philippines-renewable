const DetailsScreen = (props: any) => {
  return (
    <>
      <div className="details-screen fade-in" id="thread-content">
        <div className="top-bar">
          <button
            className="btn btn fade-in"
            onClick={() => {
              props.setScreen("home");
            }}
          >
            <i className="la la-arrow-circle-left" />
          </button>
          <span>{props.title}</span>
        </div>
        <div className="sidebar-content">{props.children}</div>
      </div>
    </>
  );
};

export default DetailsScreen;
