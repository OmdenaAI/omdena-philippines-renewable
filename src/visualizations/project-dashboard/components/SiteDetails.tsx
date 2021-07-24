import { useEffect } from "react";
import {
  fetchGlobalMapdata,
  gaPV,
  measureCoordDistance,
  numberWithCommas,
} from "./Utils";
import {
  BarChart,
  RadialAreaChart,
  RadialAxis,
  PieChart,
  PieArcSeries,
} from "reaviz";
import { useState } from "react";

const SiteDetails = (props: any) => {
  const data = props.data;

  const [powerStationsData, setPSData] = useState<any>([]);
  const [emissionsData, setEmissions] = useState<any>([]);
  const [nearbyAreas, setNearbyAreas] = useState<any>([]);
  const [stations, setStationData] = useState<any>([]);

  let powerStations: any = fetchGlobalMapdata();
  let psCount: any = [];
  let emData: any = [];
  let totalEmissions = 0;
  let nearAreas: any = [];
  let nearPowerStations: any = [];

  const power_station_images: any = {
    Solar:
      "https://images.unsplash.com/photo-1521618755572-156ae0cdd74d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=100&q=10",
    Coal: "https://images.unsplash.com/photo-1622641170740-3f45d655c4b8?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    Biomass:
      "https://images.unsplash.com/photo-1582282352927-04277241ea93?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    "Natural Gas":
      "https://images.unsplash.com/photo-1509390288171-ce2088f7d08e?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    Wind: "https://images.unsplash.com/photo-1548337138-e87d889cc369?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    "Oil-Based":
      "https://images.unsplash.com/photo-1585252155261-cff31944d781?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    Hydroelectric:
      "https://images.unsplash.com/photo-1593318939199-3e82843af95e?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
    Geothermal:
      "https://images.unsplash.com/photo-1606400767662-e6fbecaa58b3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=10",
  };

  useEffect(() => {
    let sidebarContainer: any = document.querySelector(".sidebar");
    gaPV(`Site Details`);
    setTimeout(() => {
      sidebarContainer.scroll({ top: 0, behavior: "smooth" });
    }, 200);

    powerStations = powerStations
      .filter((z: any) => z.power_station)
      .forEach((x: any) => {
        let psInstance = psCount.find((y: any) => y.key === x.category);

        if (psInstance) {
          psInstance.data += 1;
        } else {
          psCount.push({
            id: Math.random(),
            key: x.category,
            data: 1,
          });
        }
      });

    setPSData(psCount);

    // plot GHG emissions data from DOE dataset
    fetchGlobalMapdata()
      .filter((z: any) => z.power_station)
      .forEach((x: any) => {
        let psInstance = emData.find((y: any) => y.key === x.category);

        if (psInstance) {
          psInstance.data += Number(x.installed_g_co2_eq);
        } else {
          emData.push({
            key: x.category,
            data: Number(x.installed_g_co2_eq),
          });
        }

        totalEmissions += Number(x.installed_g_co2_eq);
      });

    emData.forEach((x: any) => {
      if (x.data !== 0) {
        x.data = (x.data / totalEmissions) * 100;
      } else {
        x.data = 0;
      }
    });

    emData = emData.sort((a: any, b: any) => b.data - a.data);

    setEmissions(emData);

    // produce data for the nearby areas to explore

    fetchGlobalMapdata()
      .filter((z: any) => z.suggested_area)
      .forEach((x: any) => {
        x.distanceFromArea = measureCoordDistance(
          data.latitude,
          data.longitude,
          x.latitude,
          x.longitude,
          "k"
        );
        nearAreas.push(x);
      });

    nearAreas = nearAreas.sort(
      (a: any, b: any) => a.distanceFromArea - b.distanceFromArea
    );

    setNearbyAreas(nearAreas);

    // process data for nearby power stations from the selected area
    fetchGlobalMapdata()
      .filter((z: any) => z.power_station)
      .forEach((item: any) => {
        item.distance = measureCoordDistance(
          data.latitude,
          data.longitude,
          item.latitude,
          item.longitude,
          "k"
        );
        nearPowerStations.push(item);
      });

    nearPowerStations.sort((a: any, b: any) => a.distance - b.distance);

    setStationData(nearPowerStations);
  }, [props.data]);

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
          src="https://images.unsplash.com/photo-1592833159117-ac790d4066e4?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=20"
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

        <h3 className="mt-4">
          <i className="la la-bolt text-primary" /> Powerplants nearby this
          area:
        </h3>
        <p>Powerplants that can be found nearby this suggested area.</p>
        <div className="contributors">
          {stations.slice(0, 2).map((item: any, index: number) => {
            return (
              <div className="contributor cursor-default" key={index}>
                <img
                  src={power_station_images[item.category]}
                  className="avatar avatar-lg"
                />
                <div className="info">
                  <span className="name">{item.facility_name}</span>
                  <span className="info">
                    {item.category} ({item.connection_type})
                  </span>
                  <span className="info">
                    Installed Capacity: {item.installed_capacity_mw} MW
                  </span>
                </div>
              </div>
            );
          })}
        </div>
        <h3 className="mt-4">
          <i className="la la-map text-primary mr-1" />
          Explore Nearby Areas:
        </h3>

        <div className="area-explorer">
          {nearbyAreas.slice(1, 100).map((item: any, index: number) => {
            return (
              <div
                className="area-item"
                key={index}
                onClick={() => {
                  let markerItem: any = document.querySelector(
                    `#mk-${item.id}`
                  );
                  if (markerItem) {
                    markerItem.click();
                  }
                }}
              >
                <img
                  src="https://images.unsplash.com/photo-1536481046830-9b11bb07e8b8?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=10"
                  alt="area image"
                />
                <span>
                  <strong>{item.municipality}</strong>
                </span>
                <span className="text-primary">
                  {item.distanceFromArea.toFixed(3)} km
                </span>
              </div>
            );
          })}
        </div>

        <hr />

        <h2 className="mt-4">Energy scene in the Philippines</h2>

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

        <h2 className="mt-4">Need for renewable energy</h2>
        <p>
          Using the Department of energy dataset we can see which types of power
          sources contribute most to greenhouse gas emissions from power plants
          in the Philippines.
        </p>
        <div className="ml-3">
          <PieChart
            width={300}
            height={230}
            data={emissionsData}
            series={
              <PieArcSeries
                cornerRadius={3}
                padAngle={0.02}
                padRadius={200}
                doughnut={true}
                colorScheme={["#bc5090", "#ff6361", "#ffa600"]}
              />
            }
          />
        </div>

        <ol className="list-item mt--3 pl-4">
          {emissionsData.map((x: any) => {
            return (
              <li>
                <strong>{x.key}</strong> - {x.data.toFixed(3)}%
              </li>
            );
          })}
        </ol>

        <p>
          From this breakdown we can see that Coal, Oil-based, and Natural Gas
          Powerplants are the top 3 most significant sources of Greenhouse gas
          emissions, which contribute to pollution and climate change, further
          emphasizing the need for renewable and cleaner energy sources.
        </p>

        <h2 className="mt-4">
          <i className="la la-map text-primary mr-1" />
          Explore Other Areas:
        </h2>

        <div className="area-explorer">
          {[...nearbyAreas]
            .map((ix: any) => {
              ix.rid = Math.random();
              return ix;
            })
            .sort((a: any, b: any) => a.rid - b.rid)
            .slice(1, 100)
            .map((item: any, index: number) => {
              return (
                <div
                  className="area-item"
                  key={index}
                  onClick={() => {
                    let markerItem: any = document.querySelector(
                      `#mk-${item.id}`
                    );
                    if (markerItem) {
                      markerItem.click();
                    }
                  }}
                >
                  <img
                    src="https://images.unsplash.com/photo-1526731955462-f6085f39e742?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=30"
                    alt="area image"
                  />
                  <span>
                    <strong>{item.municipality}</strong>
                  </span>
                  <span className="text-primary">
                    {item.distanceFromArea.toFixed(3)} km
                  </span>
                </div>
              );
            })}
        </div>

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

        <div className="d-flex justify-content-center">
          <button
            className="btn btn-default"
            onClick={() => {
              props.setScreen("about");
            }}
          >
            <i className="la la-user" /> Contributors
          </button>
          <button
            className="btn  btn-default"
            onClick={() => {
              props.setScreen("research");
            }}
          >
            <i className="la la-chart-line" /> Research
          </button>
        </div>
      </div>
    </>
  );
};

export default SiteDetails;
