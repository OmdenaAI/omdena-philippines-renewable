import { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import {
  currentLocation,
  fetchGlobalMapdata,
  gaPV,
  gaUE,
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
      style: MovesStyle,
      center: [120.979, 15.0941],
      zoom: 7.3,
      minZoom: 6,
      maxPitch: 65, // pitch in degrees
      maxBearing: -65, // bearing in degrees
    });

    map.on("load", () => {
      map.addSource("energy_demand", {
        type: "geojson",
        // Use a URL for the value for the `data` property.
        data: "/geojson_maps/task2_energy_demand.json",
      });

      map.addLayer({
        id: "demand_polygon_lines",
        type: "line",
        source: "energy_demand",
        paint: {
          "line-color": "#fff",
          "line-width": 0.3,
          "line-opacity": 0.3,
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
              [0.2, "transparent"],
              [0.4, "#00ccff"],
              [1, "#66ffff"],
            ],
          },
          "fill-opacity": 0.2,
        },
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
            nmarker.suggested_area ? "suggested-area" : ""
          }" id="mk-${nmarker.id}">
            <div class="marker-info">
          <div class="marker-info-content">
          <div class="content">
          <span>${nmarker.facility_name}</span>
          <small>${nmarker.municipality}</small>
          </div>

            <small class="badge ${
              nmarker.suggested_area ? "badge-success" : "badge-primary"
            } m-2">${
            nmarker.suggested_area
              ? "Suggested Area"
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
      gaUE("(Zoom) ap Exploration");
      gaPV("(Zoom) Map Exploration");
    });

    map.on("dragend", function () {
      gaUE("(Drag) Map Exploration");
      gaPV("(Drag) Map Exploration");
    });

    // bind events to trigger buttons
    let mapJump: any = document.getElementById("mapJump");
    let markerTrigger: any = document.getElementById("load-markers");

    mapJump.onclick = () => {
      flytoLocation();
    };

    markerTrigger.onclick = () => {
      renderMarkers();
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

        <div>
          <div id="map" className="absolute top right left" />
        </div>
      </>
    </>
  );
};

export default MapInterface;
