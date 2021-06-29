import axios from "axios";
import { useEffect, useState } from "react";
import DetailsScreen from "./DetailsScreen";

const Sidebar = () => {
  const [areas, setAreas] = useState<any>(null);
  const [screen, setScreen] = useState<string>("home");

  const fetchData = () => {
    axios.get("/api/doe_dataset").then((res: any) => {
      let solarAreas = res.data.filter((x: any) => x.category === "Solar");
      setAreas(solarAreas);
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <div className="sidebar">
        {screen === "details" && (
          <DetailsScreen setScreen={setScreen}>
            <div className="cover-card fade-in dl-2">
              <span className="mt-auto">
                Potential Sites for Solar Power Stations in the Philippines
              </span>
            </div>
          </DetailsScreen>
        )}

        {screen === "research" && (
          <DetailsScreen setScreen={setScreen}>
            <h1>Research</h1>
          </DetailsScreen>
        )}

        {screen === "about" && (
          <DetailsScreen setScreen={setScreen}>
            <h1>About the project</h1>
          </DetailsScreen>
        )}

        {screen === "home" && (
          <>
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
                <span
                  onClick={() => {
                    setScreen("research");
                  }}
                >
                  NOTEBOOKS
                </span>
                <span
                  onClick={() => {
                    setScreen("about");
                  }}
                >
                  About the project
                </span>
              </div>
            </div>

            <div className="sidebar-content">
              <div className="cover-card fade-in dl-2">
                <span className="mt-auto">
                  Potential Sites for Solar Power Stations in the Philippines
                </span>
              </div>

              {areas &&
                areas.map((data: any, index: number) => {
                  return (
                    <div
                      className="card-item"
                      key={index}
                      onClick={() => {
                        setScreen("details");
                      }}
                    >
                      <div className="card-item-content">
                        <div className="score-card">
                          <span>
                            <i className="la la-sun" />
                          </span>
                        </div>

                        <div className="card-info">
                          <span>{data.municipality}</span>
                          <div className="tag-row mt-1">
                            <small className="badge badge-primary mr-1">
                              {data.facility_name}
                            </small>
                            <small className="badge badge-default">
                              {data.connection_type}
                            </small>
                          </div>
                        </div>
                      </div>
                      <i className="la la-chevron-circle-right la-2x" />
                    </div>
                  );
                })}
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default Sidebar;
