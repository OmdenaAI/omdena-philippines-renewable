import type { NextApiRequest, NextApiResponse } from "next";
import { guid } from "../../components/Utils";
import DOE_dataset from "./doe_powerstations_dataset.json";
import PH_brgy from "./ph_clustered.json";
const GeoJsonGeometriesLookup = require("geojson-geometries-lookup");
const polygonCenter = require("geojson-polygon-center");
const fs = require("fs");

const geoLookup = new GeoJsonGeometriesLookup(PH_brgy);

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];
  dataset.forEach((x: any) => {
    x.id = guid();
    if (x.connection_type === "Off-Grid") {
      x.suggested_area = true;
    }
  });

  // get baraggay using GeoJSON Lookup
  // coordinates format: [lng, lat]
  const getBaranggay = (coordinates: any, index: number) => {
    let targetCoordinates = { type: "Point", coordinates: coordinates };
    let result = geoLookup.getContainers(targetCoordinates, {
      ignorePoints: false,
    });

    if (result.features.length) {
      let polygonGeo: any = result.features[0].geometry;
      // let center = polygonCenter(polygonGeo);
      // center.coordinates = [long,lat]
      let ccoord = polygonGeo.coordinates[0][6];
      if (ccoord) {
        dataset[index].latitude = ccoord[1];
        dataset[index].longitude = ccoord[0];
      } else {
        console.log("failed to get polygon");
      }
      // return polygonGeo.coordinates[0][0];
    } else {
      return false;
    }
  };

  // correct coordinates based on Philippines baranggay datasets

  dataset.forEach((x: any, index: number) => {
    getBaranggay([x.longitude, x.latitude], index);
  });

  // sort the dataset to prioritize lower operating hours
  dataset = dataset
    .sort(
      (a: any, b: any) =>
        parseFloat(a.operating_hours) - parseFloat(b.operating_hours)
    )
    .filter((x: any) => x.latitude);

  // let d2: any = PH_brgy;

  fs.writeFile("./doe_v1.json", JSON.stringify(dataset), (err: any) => {
    if (err) {
      console.error(err);
      return;
    }
    //file written successfully
    console.log("file updated!");
  });

  res.send(dataset);
  return req;
};
