import { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import {
  currentLocation,
  fetchGlobalMapdata,
  gaPV,
  gaUE,
  getFillOpacity,
  isMobile,
  MovesStyle,
} from "./Utils";

// replace with your own access token from Mapbox.
mapboxgl.accessToken =
  "pk.eyJ1IjoiYnJ5Y2UwNiIsImEiOiJjazNmbndybm4wMDk3M29wZ2dicjlmb29iIn0.NVknKG525ZpQVmIAbFiqfw";

const MapInterface = (props: any) => {
  useEffect(() => {
    // start new Mapbox Instance
    const map = new mapboxgl.Map({
      container: document.getElementById("map"),
      style: localStorage.mapStyle ? localStorage.mapStyle : MovesStyle,
      center: [120.979, 15.0941],
      zoom: 7.3,
      minZoom: 6,
      maxPitch: 65, // pitch in degrees
      maxBearing: -65, // bearing in degrees
    });

    map.on("load", () => {
      map.addSource("energy_demand", {
        type: "geojson",
        data: "/geojson_maps/task2_energy_demand.json",
      });

      map.addSource("correlated_data", {
        type: "geojson",
        data: "/geojson_maps/correlated_v1.json",
      });

      map.addLayer({
        id: "data-points",
        type: "circle",
        source: "correlated_data",
        paint: {
          "circle-color": localStorage.pointColor
            ? localStorage.pointColor
            : "#59ffde",
          "circle-radius": 3,
          "circle-opacity": 0.7,
        },
      });

      map.addLayer({
        id: "demand_polygon_lines",
        type: "line",
        source: "energy_demand",
        paint: {
          "line-color": "#fff",
          "line-width": 0.3,
          "line-opacity": 0.2,
        },
      });

      map.addLayer({
        id: "demand-fill",
        type: "fill",
        source: "energy_demand",
        layout: {},
        paint: {
          "fill-color": {
            property: "Response",
            stops: [
              [0.0, "#0B1C71"],
              [0.2, "#1C4998"],
              [0.4, "#1D7EB3"],
              [0.6, "#36A8B8"],
              [0.8, "#BCE6A5"],
              [1, "#FEFFC1"]
            ],
          },
          "fill-opacity": getFillOpacity(),
        },
      });

      let popup = new mapboxgl.Popup({
        ponterEvents: "none",
      });

      // create pop up on click
      map.on("mouseenter", "data-points", function (e: any) {
        let markerUI = `
        <div class="map-marker 
         suggested-area active-marker">
          <div class="marker-info">
        <div class="marker-info-content">
        <div class="content">
        <span>Suggested Settlement</span>
        <small>Population: ${e.features[0].properties.POP1.toFixed(1)}</small>
        </div>
          <small class="badge badge-success">
             Point Information
        </small>
         </div>
         </div>
          </div>
        `;
        popup.setLngLat(e.lngLat);

        popup.setHTML(markerUI);
        popup.addTo(map);

        gaUE("Hover: Point Info View");
        gaPV("Hover: Point Info View");
      });
    });

    const flytoLocation = () => {
      console.log("dest=>", props.coordinates);
      map.flyTo({
        center: [currentLocation().lng, currentLocation().lat],
        zoom: map.getZoom(),
        speed: 1.25,
        essential: true,
      });
    };

    const renderMarkers = () => {
      let markersData: any = fetchGlobalMapdata();
      let existingMarker = document.querySelector(".map-marker");

      if (!existingMarker) {
        markersData.forEach((nmarker: any, index: number) => {
          var elx = document.createElement("div");
          elx.className = `marker-location-update lu-${index}`;
          elx.onclick = () => {
            if (nmarker.suggested_area) {
              props.selectArea(nmarker);
              gaPV("Site Detail View | Map Click", `${nmarker.municipality}`);
            }
          };
          elx.onmouseenter = () => {
            gaUE("Interaction: Viewing marker details");
            gaPV(`${nmarker.municipality} | Marker Details`);
          };
          elx.innerHTML = `

          <div class="map-marker ${
            nmarker.suggested_area ? "suggested-area area-marker" : ""
          }" id="mk-${nmarker.id}">
            <div class="marker-info ${
              nmarker.suggested_area ? "suggested-area area-marker" : ""
            }">
          <div class="marker-info-content">
          <div class="content">
          <span>${nmarker.facility_name}</span>
          <small>${nmarker.municipality}</small>
          </div>

            <small class="badge ${
              nmarker.suggested_area ? "badge-info" : "badge-primary"
            } m-2">${
            nmarker.suggested_area
              ? "AREA MARKER"
              : `${nmarker.category} Powerplant`
          }</small>
           </div>
           <div class="info-point"></div>
           </div>
            <div class="marker ${
              nmarker.suggested_area
                ? "suggested-area"
                : nmarker.category.replace(" ", "")
            }"></div>
            </div>
          `;
          new mapboxgl.Marker(elx)
            .setLngLat([nmarker.longitude, nmarker.latitude])
            .addTo(map);
        });
      }

      // ease map

      if (!isMobile()) {
        map.easeTo({
          padding: { left: 320 },
          duration: 1000,
        });
      }
    };

    // detect zooming on map to measure engagement

    map.on("zoomend", function () {
      gaUE("(Zoom) Map Exploration");
      gaPV("(Zoom) Map Exploration");
    });

    map.on("dragend", function () {
      gaUE("(Drag) Map Exploration");
      gaPV("(Drag) Map Exploration");
    });

    const changeMapStyle = () => {
      map.setStyle("mapbox://styles/mapbox/satellite-v9");
    };

    // bind events to trigger buttons
    let mapJump: any = document.getElementById("mapJump");
    let markerTrigger: any = document.getElementById("load-markers");
    let styleChangeTrigger: any = document.getElementById("change-map-style");

    mapJump.onclick = () => {
      flytoLocation();
    };

    markerTrigger.onclick = () => {
      renderMarkers();
    };

    styleChangeTrigger.onclick = () => {
      changeMapStyle();
    };
  }, []);

  // fly to location when the coordinates props are set
  useEffect(() => {
    let mapJump: any = document.getElementById("mapJump");
    mapJump.click();
  }, [props.coordinates]);

  return (
    <>
      <>
        <button id="mapJump" className="d-none" />

        <button id="load-markers" className="d-none" />

        <button id="change-map-style" className="d-none" />

        <div>
          <div id="map" className="absolute top right left" />
        </div>
      </>
    </>
  );
};

export default MapInterface;
