import "toastify-js/src/toastify.css";
import "../styles/animations.scss";
import "../styles/sidebar.scss";
import "../styles/markers.scss";
import "../styles/globals.scss";
import "mapbox-gl/dist/mapbox-gl.css";

// import App from "next/app";
import type { AppProps /*, AppContext */ } from "next/app";

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

// Only uncomment this method if you have blocking data requirements for
// every single page in your application. This disables the ability to
// perform automatic static optimization, causing every page in your app to
// be server-side rendered.
//
// MyApp.getInitialProps = async (appContext: AppContext) => {
//   // calls page's `getInitialProps` and fills `appProps.pageProps`
//   const appProps = await App.getInitialProps(appContext);

//   return { ...appProps }
// }

export default MyApp;
