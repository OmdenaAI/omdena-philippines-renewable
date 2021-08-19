import { useEffect, useState } from "react";
import {
  ColoredStyle,
  lightMapStyle,
  MovesStyle,
  satelliteStyle,
} from "../components/Utils";

const MapStyleSelector = () => {
  const styleSet: any = [
    {
      name: "dark",
      pointColor: "#59ffde",
      mapStyle: MovesStyle,
    },
    {
      name: "light",
      pointColor: "#366de3",
      mapStyle: lightMapStyle,
    },
    {
      name: "street",
      pointColor: "#366de3",
      mapStyle: ColoredStyle,
    },
    {
      name: "satellite",
      pointColor: "#59ffde",
      mapStyle: satelliteStyle,
    },
  ];

  const [mapMode, setMode] = useState<string>("");

  useEffect(() => {
    if (localStorage.mapMode) {
      setMode(localStorage.mapMode);
    } else {
      setMode("satellite");
    }
  }, []);

  return (
    <>
      <h4>
        <i className="la la-map text-primary" /> Change Map Mode
      </h4>
      <div className="map-styles mb-3 fade-in">
        {styleSet.map((x: any, index: number) => {
          return (
            <div
              className={`map-style ${x.name} ${
                mapMode === x.name ? "active-mode" : ""
              }`}
              key={index}
              onClick={() => {
                localStorage.mapStyle = x.mapStyle;
                localStorage.pointColor = x.pointColor;
                localStorage.mapMode = x.name;
                window.location.reload();
              }}
            >
              <span>{x.name}</span>
            </div>
          );
        })}
      </div>
    </>
  );
};

export default MapStyleSelector;
