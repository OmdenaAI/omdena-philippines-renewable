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