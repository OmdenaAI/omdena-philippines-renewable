import { useEffect } from "react";
import { gaPV } from "./Utils";

const SiteDetails = (props: any) => {
  const data = props.data;

  // let values: any = Object.values(data);

  useEffect(() => {
    let sidebarContainer: any = document.querySelector(".sidebar");
    gaPV(`Site Details`);
    setTimeout(() => {
      sidebarContainer.scroll({ top: 0, behavior: "smooth" });
    }, 200);
  }, []);

  return (
    <>
      <div className="banner-image">
        <span className="mt-auto">{data.municipality}</span>
      </div>
      <br />
      <br />
      <br />
      <br />
      <br />

      <div className="research-tab px-1 mt-5 pt-5">
        <h3 className="mt-0">Living in Darkness</h3>
        <p>
          During nighttime, light intensity in{" "}
          <span className="text-primary">{data.municipality}</span> is{" "}
          <span className="text-primary">[DATA]</span> dimmer across{" "}
          <span className="text-primary">{data.province}</span>,{" "}
          <span className="text-primary">[DATA]</span> across{" "}
          <span className="text-primary">{data.region}</span>
          and <span className="text-primary">[DATA]</span> versus{" "}
          <span className="text-primary">Metro Manila</span>.
        </p>

        <h3 className="mt-0">Lacking in Energy</h3>
        <p>
          From PSA 2018 data there are{" "}
          <span className="text-primary">[DATA] people</span> living in{" "}
          <span className="text-primary">{data.municipality}</span>. Based on
          our estimates, there are approximately{" "}
          <span className="text-primary">[DATA] households & settlements</span>{" "}
          in the area.
        </p>
        <p>
          The <span className="text-primary">[DATA] power plants</span> within
          [DATA] radius can provide around{" "}
          <span className="text-primary">[DATA]</span> kWh, amounting to only{" "}
          <span className="text-primary">[DATA] hours</span> of power daily,
          complemented by rotational brownouts.
        </p>
        <p>
          Considering [COMPUTE] kWh is needed in order to have a continuous
          supply of electricity throughout the day, there is a deficit of nearly
          [COMPUTE] kWH.
        </p>

        <h3 className="mt-4">Hope in Solar Energy</h3>
        <p>
          We’ve estimated that installing a solar microgrid in this area could
          generate:
          {/* <p>based on the SolarGIS dataset the mean voltage output of this area is around: </p> */}
          <h2 className="text-primary">[DATA] kWh</h2>
          In estimating the solar energy capacity, we’ve used (solar irradiance,
          elevation - please add more).
        </p>

        <h3 className="mt-4">Living in Light</h3>
        <p>
          The energy that solar can add is [EVAL] to mitigate the energy poverty
          of <span className="text-primary">{data.municipality}</span>. By
          having a solar microgrid,{" "}
          <span className="text-primary">[DATA] kWh</span> of energy could
          supply the [DATA] households in the area.
        </p>
        <p>
          Additionally, using solar could also save us [COMPUTE] tons of CO2
          emissions and
          <span className="text-primary">[DATA]</span> months in installation
          time compared to other energy sources. Providing enough power will
          hasten further economic development.
        </p>
        <h2 className="text-primary">{data.accumulated_installed_g_co2_eq}</h2>

        {/* <h3 className="mt-5">Addition Information</h3> */}

        {/* {data &&
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
        })} */}
      </div>
    </>
  );
};

export default SiteDetails;
