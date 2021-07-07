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
    <div className="research-tab px-1">
      <div className="cover-card fade-in dl-2 flex-column">
        <h2 className="mt-auto text-white mb--1">{data.municipality}</h2>
        {/* <span className="text-white">{data.municipality}</span> */}
      </div>

      <h3 className="mt-0">Why is this area ideal for solar power stations?</h3>
      <p>
        <span className="text-primary">{data.municipality}</span> is under the{" "}
        <span className="text-primary">{data.island_grid}</span> island region
        and this area currently relies on an{" "}
        <span className="text-primary">
          {data.category}, {data.subcategory} Powerstation.
        </span>{" "}
        This powerstation operates for{" "}
        <span className="text-primary">{data.operating_hours} hours</span> a
        day. And has a dependable power capacity of{" "}
        <span className="text-primary">
          {data.dependable_capacity_mw} Mega Watts.
        </span>
      </p>

      <h3 className="mt-4">Home much energy can be produced with Solar Panels around this area?</h3>
      <p>based on the SolarGIS dataset the mean voltage output of this area is around: </p>
      <h2 className="text-primary">{data.PVOUT_mean.toFixed(2)} Kw/h</h2>

      <small><strong>What can you do with this amount of power?</strong></small>

      <h3 className="mt-5">Addition Information</h3>

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
    </div>
  );
};

export default SiteDetails;
