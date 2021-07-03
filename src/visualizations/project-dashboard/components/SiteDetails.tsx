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

      <h3 className="mt-4">Power availability of Solar Energy</h3>
      <p>Power availability in the philippines based on solar irradiance.</p>
      <img
        src="https://scontent.fcrk1-1.fna.fbcdn.net/v/t1.15752-9/211617769_962118731276406_4961368663717972900_n.png?_nc_cat=109&ccb=1-3&_nc_sid=ae9488&_nc_ohc=--UELWDLVtMAX-S19Ka&tn=4NS8_AonkdOm5ozy&_nc_ht=scontent.fcrk1-1.fna&oh=c35ebecaeeb91317d840279216b63773&oe=60E4E5F7"
        className="img-fluid"
      />

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
