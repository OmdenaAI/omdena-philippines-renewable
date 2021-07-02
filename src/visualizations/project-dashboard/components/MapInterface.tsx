import { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import { currentLocation, fetchGlobalMapdata, MovesStyle } from "./Utils";

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
          //:TODO complete marker render functions

          var elx = document.createElement("div");
          elx.className = `marker-location-update lu-${index}`;
          elx.onclick = () => {
            if (nmarker.connection_type === "Off-Grid") {
              props.selectArea(nmarker);
            }
          };
          elx.innerHTML = `

          <div class="map-marker ${nmarker.connection_type}" id="mk-${
            nmarker.id
          }">
          <div class="marker-info">
          <div class="marker-info-content">
            <span>${nmarker.facility_name}</span>
            <small>${nmarker.municipality}</small>
            </div>
          <div class="info-point"></div>
          </div>
          <div class="marker ${nmarker.category.replace(" ", "")}   ${
            nmarker.connection_type
          }"></div>
        </div>
          `;
          new mapboxgl.Marker(elx)
            .setLngLat([nmarker.longitude, nmarker.latitude])
            .addTo(map);
        });
      }

      // ease map

      map.easeTo({
        padding: { left: 320 },
        duration: 1000,
      });
    };

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
