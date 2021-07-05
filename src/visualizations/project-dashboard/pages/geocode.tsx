import Layout from "../components/Layout";
import rawdata from "./api/doe_powerstations_dataset.json";
import { useState, useEffect } from "react";
import axios from "axios";

const GeoCode = () => {
  const [data, setData] = useState<any>([]);
  const [percentage, setPercentage] = useState(0);
  const [query, setQuery] = useState("");

  const GOOGLE_MAPS_APIKEY = "YOUT API KEY";

  const startCorrection = () => {
    data.forEach((x: any, index: number) => {
      let addr = x.municipality;
      setTimeout(() => {
        axios
          .get(
            `https://maps.googleapis.com/maps/api/geocode/json?address=${addr}&key=${GOOGLE_MAPS_APIKEY}`
          )
          .then((res: any) => {
            if (res.data) {
              if (res.data.results.length !== 0) {
                // console.log("SUCCESS!")
                let coords = res.data.results[0].geometry.location;
                let address = x.municipality;
                let d1 = [...data];
                d1[index].latitude = coords.lat;
                d1[index].longitude = coords.lng;
                d1[index].corrected = true;

                let percent =
                  (data.filter((y: any) => y.corrected).length / data.length) *
                  100;
                setPercentage(percent);
                setData(data);
                setQuery(address);
              } else {
                let address = x.municipality;
                let d1 = [...data];
                d1[index].corrected = false;
                setData(data);
                setQuery(address);
                let percent =
                  (data.filter((y: any) => y.corrected).length / data.length) *
                  100;
                setPercentage(percent);
              }
            }
          });
      }, index * 2000);
    });
  };

  // test fetch
  const testFetch = () => {
    axios
      .get(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${"Limay, Bataan"}&key=${GOOGLE_MAPS_APIKEY}`
      )
      .then((res) => {
        console.log(res.data.results.length);
      });
  };

  useEffect(() => {
    setData(rawdata);
  }, []);
  return (
    <Layout>
      <div className="m-5">
        <h1>Geocoding System</h1>
        <p>Correcting GeoJSON data</p>
        <p>
          <strong>Query Location Name: {query}</strong>
        </p>
        <p className="text-danger">
          <strong>
            <i className="la la-times-circle" /> Failed Location correction:{" "}
            {data.filter((x: any) => !x.corrected).length}
          </strong>
        </p>
        <strong className="text-primary">
          Progress: {data.filter((x: any) => x.corrected).length}/{data.length}{" "}
          ({percentage}%)
        </strong>
        <div className="progress mt-3">
          <div
            className="progress-bar bg-gradient-success"
            role="progressbar"
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
        {percentage === 0 && (
          <>
            <button className="btn btn-default" onClick={startCorrection}>
              Start Correction
            </button>

            <button className="btn btn-primary" onClick={testFetch}>
              Test Fetch
            </button>
          </>
        )}
        <textarea
          placeholder="JSON data"
          className="p-3 mt-3"
          id="text-box"
          value={JSON.stringify(data)}
        />

        <br />
        <br />
        <h2>Failed Location List</h2>
        <ol>
          {data
            .filter((x: any) => !x.corrected)
            .map((x: any) => {
              return <li>{x.municipality}</li>;
            })}
        </ol>
      </div>
    </Layout>
  );
};

export default GeoCode;
