import { useEffect } from "react";

const SiteDetails = (props: any) => {
  const data = props.data;

  let values: any = Object.values(data);

  useEffect(() => {
    let sidebarContainer: any = document.querySelector(".sidebar");
    setTimeout(() => {
      sidebarContainer.scroll({ top: 0, behavior: "smooth" });
    }, 200);
  }, []);

  return (
    <>
      <div className="cover-card fade-in dl-2 flex-column">
        <h2 className="mt-auto text-white mb--1">{data.facility_name}</h2>
        <small className="text-white">{data.municipality}</small>
      </div>

      {data &&
        Object.keys(data).map((x: any, index: number) => {
          return (
            <div className="card border info-card" key={index}>
              <div className="header">
                <small>
                  <i className="la la-cube text-primary" />{" "}
                  {x.split("_").join(" ")}
                </small>
              </div>
              {x !== "icon" && (
                <span className="px-3 py-2">
                  {values[index] ? values[index] : "N/A"}
                </span>
              )}
            </div>
          );
        })}
    </>
  );
};

export default SiteDetails;
