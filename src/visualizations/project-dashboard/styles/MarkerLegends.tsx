import { useEffect, useState } from "react";

const MarkerLegends = () => {
  const MarkerLabels: any = [
    {
      name: "Area Marker",
      classification: "Off-Grid",
    },
    {
      name: "Suggested Areas",
      classification: "pointer-marker",
    },
    {
      name: "Solar Power Station",
      classification: "Solar",
    },
    {
      name: "Hydroelectric Powerplant",
      classification: "Hydroelectric",
    },
    {
      name: "Geothermal Powerplant",
      classification: "Geothermal",
    },
    {
      name: "Wind Power Station",
      classification: "Wind",
    },
    {
      name: "Oil Power Station",
      classification: "Oil-Based",
    },
    {
      name: "Natural Gas Powerplant",
      classification: "NaturalGas",
    },
    {
      name: "Biomass Powerplant",
      classification: "Biomass",
    },
    {
      name: "Coal-fired Powerstation",
      classification: "Coal",
    },
  ];

  const [pointColor, setpointColor] = useState<string>("#59ffde");
  const [mapMode, setMapMode] = useState<string>("dark");

  useEffect(() => {
    if (localStorage.pointColor) {
      setpointColor(localStorage.pointColor);
      setMapMode(localStorage.mapMode);
    }
  }, []);

  return (
    <div className="marker-infos">
      <div className="marker-legends fade-in-bottom">
        <small>
          <i className="la la-map-marker text-info" /> Marker Labels
        </small>

        <ul className="pt-1">
          {MarkerLabels.map((item: any, index: number) => {
            return (
              <li key={index}>
                <div
                  style={{
                    backgroundColor:
                      item.classification === "pointer-marker"
                        ? pointColor
                        : "#59ffde",
                  }}
                  className={`label-icon ${item.classification}`}
                />

                {item.name}
              </li>
            );
          })}
        </ul>
      </div>

      <div className="marker-legends fade-in-bottom">
        <small>
          <i className="la la-bolt text-info" /> ENERGY ACCESS
        </small>
        <ul>
          <div className="progress mt-3">
            <div
              className={`progress-bar energy-demand-gradient ${mapMode}`}
              role="progressbar"
              style={{ width: "100%" }}
            ></div>
          </div>
          <div className="labels">
            <span>No Access</span>
            <span>Has Access</span>
          </div>
        </ul>
      </div>
    </div>
  );
};

export default MarkerLegends;
