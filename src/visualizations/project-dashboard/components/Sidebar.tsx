import axios from "axios";
import { useEffect, useState } from "react";
import DetailsScreen from "./DetailsScreen";
import ReasearchTab from "./ResearchTab";
import AboutTab from "./AboutTab";
import SiteDetails from "./SiteDetails";
import { gaPV, gaScroll, gaUE, setGlobalMapdata, startPageLoad, stopPageLoad } from "./Utils";

const Sidebar = (props: any) => {
  const [areas, setAreas] = useState<any>(null);
  const [screen, setScreen] = useState<string>("home");
  const [selectedSite, selectSite] = useState<any>(null);
  const [query, setQuery] = useState<any>("")

  const sidebarScrollTop = () => {
    let sidebarContainer: any = document.querySelector(".sidebar");

    sidebarContainer.scroll({ top: 0 });
  };

  const fetchData = () => {
    axios.get("/api/correlated_dataset").then((res: any) => {
      let suggestedAreas = res.data.filter(
        (x: any) => x.suggested_area === true
      );
      setAreas(suggestedAreas);

      setGlobalMapdata(res.data);

      // trigger marker render
      let markerTrigger: any = document.getElementById("load-markers");
      if (markerTrigger) {
        markerTrigger.click();
      }
    });
  };

  const viewDetails = (details: any) => {
    let detailCoordinates = {
      lat: details.latitude,
      lng: details.longitude,
    };

    sidebarScrollTop();

    localStorage.coordinates = JSON.stringify(detailCoordinates);
    props.setCoordinates(detailCoordinates);
    selectSite(details);
    setScreen("details");

    // set the pointer to active state when an event is selected
    let markerItem: any = document.querySelector(`#mk-${details.id}`);
    let currentActiveMarker: any = document.querySelector(".active-marker");

    currentActiveMarker?.classList.remove("active-marker");

    // setTimeout(() => {
    if (markerItem) {
      markerItem.classList.add("active-marker");
    }
    // }, 200);
  };

  const searchDataset = (search_query:string) => {
    startPageLoad()
    axios.get(`/api/correlated_dataset?search=${search_query}`).then((res: any) => {
      let suggestedAreas = res.data.filter(
        (x: any) => x.suggested_area === true
      );
      setAreas(suggestedAreas);
      gaPV("Dataset Search",`/search/${search_query}`)
      gaUE("User Search",`/search/${search_query}`)
    
     stopPageLoad()
    });
  }

  useEffect(() => {
    fetchData();

    let sidebarThread:any = document.querySelector(".sidebar")
     sidebarThread.onscroll= () => {
       let scroll = sidebarThread.scrollTop
       if (scroll > 1200 && scroll < 1300) {
        gaPV("Content Read")
        gaScroll("Content Read Scroll")
        gaUE("Engagement","Reading Content")
      }
     }
  }, []);

  useEffect(() => {
    if (props.selectedArea) {
      viewDetails(props.selectedArea);
    }
  }, [props.selectedArea]);

  return (
    <>
      <div className="sidebar">
        {screen === "details" && (
          <DetailsScreen setScreen={setScreen} title="Location Details">
            <SiteDetails data={selectedSite} />
          </DetailsScreen>
        )}

        {screen === "research" && (
          <DetailsScreen setScreen={setScreen} title="Research">
            <ReasearchTab />
          </DetailsScreen>
        )}

        {screen === "about" && (
          <DetailsScreen setScreen={setScreen} title="About the Project">
            <AboutTab />
          </DetailsScreen>
        )}

        {screen === "home" && (
          <>
            <div className="sidebar-navigation">
              <div className="top-bar">
                <a
                  href="https://www.linkedin.com/groups/13967597"
                  target="_blank"
                >
                  <img src="/images/omdena-ph.png" />
                </a>
                <div className="mt-1 mr-2 d-flex">
                  <input
                    type="text"
                    placeholder="Search Places.."
                    className="form-control"
                    id="search-input"
                    onKeyUp={(e:any)=>{
                      setQuery(e.target.value)
                     if(e.key === "Enter"){
                      searchDataset(e.target.value)
                     }
                    }}
                  />
                  <button className="btn btn-default ml-2" 
                  onClick={()=>{
                    searchDataset(query)
                  }}
                  >
                    <i className="la la-search" />
                  </button>
                </div>
              </div>
              <div className="nav-links">
                <span className="active">Dataset</span>
                <span
                  onClick={() => {
                    setScreen("research");
                    sidebarScrollTop();
                  }}
                >
                  Research
                </span>

                <span
                  onClick={() => {
                    setScreen("about");
                    sidebarScrollTop();
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

              <h4>Sorted based on relevance</h4>

              {areas && areas.length === 0 && query.trim() !== "" && (
                <div className="mt-3 border-top py-3 fade-in-bottom">
                <h2>No results found.</h2>
                </div>
              )}

              {areas &&
                areas.map((data: any, index: number) => {
                  return (
                    <div
                      className="card-item"
                      key={index}
                      onClick={() => {
                        viewDetails(data);
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
