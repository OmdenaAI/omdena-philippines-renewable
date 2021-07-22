import { useEffect } from "react";
import { fetchGlobalMapdata, gaPV, numberWithCommas } from "./Utils";
import { BarChart, RadialAreaChart, RadialAxis } from "reaviz";
import { useState } from "react";

const SiteDetails = (props: any) => {
  const data = props.data;

  const [powerStationsData, setPSData] = useState<any>([]);

  let powerStations: any = fetchGlobalMapdata();
  let psCount: any = [];

  useEffect(() => {
    // let sidebarContainer: any = document.querySelector(".sidebar");
    gaPV(`Site Details`);
    // setTimeout(() => {
    //   sidebarContainer.scroll({ top: 0, behavior: "smooth" });
    // }, 200);

    powerStations = powerStations
      .filter((z: any) => z.power_station)
      .forEach((x: any) => {
        let psInstance = psCount.find((y: any) => y.key === x.category);

        if (psInstance) {
          psInstance.data += 1;
        } else {
          psCount.push({
            key: x.category,
            data: 1,
          });
        }
      });

    setPSData(psCount);
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
        <h2 className="mt-0">Lacking in Energy</h2>
        <p>
          According the DHS data an estimated{" "}
          <span className="text-primary">
            {numberWithCommas(data.population.toFixed(0))} people
          </span>{" "}
          living in <span className="text-primary">{data.municipality}</span>.
          In which there are approximately{" "}
          <span className="text-primary">
            {numberWithCommas(data.count)} households
          </span>{" "}
          around the area that have limited access to electricity.
        </p>

        <h2 className="mt-4">Hope in Solar Energy</h2>
        <img
          src="https://images.unsplash.com/photo-1592833159117-ac790d4066e4?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
          className="img-fluid my-2"
        />
        <p>
          Based on the{" "}
          <a
            href="https://globalsolaratlas.info/support/data-outputs"
            target="_blank"
          >
            Solar Global Atlas
          </a>{" "}
          and World Bank Dataset, Solar Panels around this area can produce the
          following amount of energy per square meter:
          <h3 className="text-primary mt-2">
            Mean PVout: {numberWithCommas(data.pvout_average_mean.toFixed(2))}{" "}
            kWh
          </h3>
          <div className="pl-3 mt-4">
            <BarChart
              height={180}
              width={320}
              data={[
                { key: "Minimum", data: data.pvout_average_min },
                { key: "Maximum", data: data.pvout_average_max },
                { key: "Mean", data: data.pvout_average_mean },
                { key: "H. Power Consumption", data: 897 },
                { key: "Households", data: data.count },
              ]}
            />
          </div>
        </p>

        <h3 className="mt--3"></h3>
        <p>
          According to the{" "}
          <a
            href="https://www.statista.com/statistics/1236746/consumption-of-electricity-per-capita-in-the-philippines/"
            target="_blank"
          >
            Statisa Research Department (2020)
          </a>
          , On average, the household electricity consumption (per capita) in
          the Philippines is about{" "}
          <span className="text-primary">897 kWh, per year</span>.
        </p>

        <p>
          And with the average Solar Energy output ranging around{" "}
          <strong className="text-primary">
            {numberWithCommas(data.pvout_average_mean.toFixed(2))} kWh
          </strong>{" "}
          (per square meter, per year) for the suggested areas of{" "}
          <strong className="text-primary">{data.municipality}</strong>, We can
          see that solar energy can be an effective power source for this area.
        </p>

        <h2 className="mt-4">Energy Scene in the Philippines</h2>

        <p>
          Based on the Department of Energy Dataset. The Power stations types in
          the Philippines are as follows:
        </p>
        <div className="mt--5">
          <RadialAreaChart
            data={powerStationsData}
            height={330}
            width={330}
            axis={<RadialAxis type="category" />}
          />
        </div>
        <p className="mt--5">
          This chart shows us that the country predominantly relies on
          Non-renewable energy sources like Oil based Power Plants which can
          harmful to the environment because of their byproducts and High
          Greenhouse gas emissions.
        </p>

        <p>
          While Hydroelectric Power plants are classified as a renewable energy
          source and are the second most prominent powerplant type in the
          country. The Philippines is still lacking in the utilization of other
          renewable energy sources like Solar, Wind, and Geothermal Powerplants,
          which highlights the need to explore opportunities to utilize these
          renewable energy sources. To help address the country's growing demand
          for energy, in a cleaner and more efficient way.
        </p>

        <hr />

        <div className="card border info-card mb-3 mt-3">
          <div className="header">
            <small>
              <i className="la la-exclamation-circle text-primary" /> Disclaimer
            </small>
          </div>
          <div className="px-3 pt-2 text-center">
            <i className="la la-cubes la-3x text-info" />
            <p className="py-1">
              This is an experimental open-source project. All of the data
              provided from this tool/web application are not absolute and may
              be subject to change in future iterations. Use this platform at
              your own risk.
            </p>
          </div>
        </div>

        <p className="py-1">
          If you have feedback, questions, or suggestions, feel free to reach
          out to the project contributors. or check out the research tab to
          learn more
        </p>

        <button
          className="btn btn-sm btn-default"
          onClick={() => {
            props.setScreen("about");
          }}
        >
          <i className="la la-user" /> See Contributors
        </button>
        <button
          className="btn btn-sm btn-default"
          onClick={() => {
            props.setScreen("research");
          }}
        >
          <i className="la la-chart-line" /> Research Tab
        </button>
      </div>
    </>
  );
};

export default SiteDetails;
