import { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import { currentLocation, MovesStyle } from "./Utils";

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

    // bind events to trigger buttons
    let mapJump: any = document.getElementById("mapJump");
    mapJump.onclick = () => {
      flytoLocation();
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
        <button id="removeRoutes" className="d-none" />

        <button id="incidents-btn" className="d-none" />
        <button id="incident-track" className="d-none" />

        <div>
          <div id="map" className="absolute top right left" />
        </div>
      </>
    </>
  );
};

export default MapInterface;
