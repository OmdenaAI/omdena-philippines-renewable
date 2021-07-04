import Toastify from "toastify-js";
import nprogress from "nprogress";

export const guid = () => {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = (Math.random() * 16) | 0,
      v = c == "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

export const Toast = (message: string) => {
  Toastify({
    text: message,
    duration: 2000,
    destination: "/analytics",
    newWindow: false,
    close: true,
    gravity: "bottom", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
    stopOnFocus: true, // Prevents dismissing of toast on hover
    onClick: function () {}, // Callback after click
  }).showToast();
};

export const startPageLoad = () => {
  nprogress.start();
};

export const stopPageLoad = () => {
  nprogress.done();
};

export const lightMapStyle =
  "https://raw.githubusercontent.com/jingsam/mapbox-gl-styles/master/Light.json";
export const HurricaneMapStyle =
  "https://raw.githubusercontent.com/jingsam/mapbox-gl-styles/master/Hurricane.json";

export const XrayMapStyle =
  "https://raw.githubusercontent.com/jingsam/mapbox-gl-styles/master/X-ray.json";

export const MovesStyle =
  "https://raw.githubusercontent.com/jingsam/mapbox-gl-styles/master/Moves-map.json";

export const currentLocation = () => {
  if (localStorage.coordinates) {
    return JSON.parse(localStorage.coordinates);
  } else {
    return { lng: 120.979, lat: 15.0941 };
  }
};

// set global map data

export const setGlobalMapdata = (data: any) => {
  const global: any = window;
  global.mapData = data;
};

export const fetchGlobalMapdata = () => {
  const global: any = window;
  return global.mapData;
};

export const isMobile = () => {
  if (process.browser) {
    if (
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      )
    ) {
      return true;
    } else {
      return false;
    }
  }
};

// measure distance between coordinates by geodata source

export function measureCoordDistance(
  lat1: any,
  lon1: any,
  lat2: any,
  lon2: any,
  unit: any
) {
  lat1 = parseFloat(lat1);
  lon1 = parseFloat(lon1);
  lat2 = parseFloat(lat2);
  lon2 = parseFloat(lon2);

  if (lat1 === lat2 && lon1 === lon2) {
    return 0;
  } else {
    var radlat1 = (Math.PI * lat1) / 180;
    var radlat2 = (Math.PI * lat2) / 180;
    var theta = lon1 - lon2;
    var radtheta = (Math.PI * theta) / 180;
    var dist =
      Math.sin(radlat1) * Math.sin(radlat2) +
      Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
    if (dist > 1) {
      dist = 1;
    }
    dist = Math.acos(dist);
    dist = (dist * 180) / Math.PI;
    dist = dist * 60 * 1.1515;
    if (unit === "K") {
      dist = dist * 1.609344;
    }
    if (unit === "N") {
      dist = dist * 0.8684;
    }
    return dist;
  }
}
