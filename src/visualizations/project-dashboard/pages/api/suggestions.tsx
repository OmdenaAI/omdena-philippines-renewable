import type { NextApiRequest, NextApiResponse } from "next";
import { guid } from "../../components/Utils";
import DOE_dataset from "./doe_v1.json";
import municipalities_data from "./ph_muncipalities.json";
import core_data_points from "../../public/geojson_maps/correlated_v1.json";
import Fuse from "fuse.js";
var polygonCenter = require("geojson-polygon-center");

const GeoJsonGeometriesLookup = require("geojson-geometries-lookup");

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];

  let muni_data = municipalities_data;
  let coreDataP: any = core_data_points;
  coreDataP = coreDataP.features;
  let suggestions: any = [];

  // init geojson geometries lookup
  const glookup = new GeoJsonGeometriesLookup(muni_data);

  // geocode area
  coreDataP.forEach((x: any) => {
    let geoSearch: any = glookup.getContainers({
      type: "Point",
      coordinates: [x.properties.Longitude, x.properties.Latitude],
    });
    let geocodeFeatures = geoSearch.features[0];
    if (geocodeFeatures) {
      let geocodeRes = geocodeFeatures.properties;
      let areaInstance = suggestions.find(
        (y: any) => y.GID_2 === geocodeRes.GID_2
      );

      //   let areaCenter = polygonCenter(geocodeFeatures.geometry);

      let suggestedArea = {
        id: guid(),
        GID_2: geocodeRes.GID_2,
        municipality: `${geocodeRes.NAME_2}, ${geocodeRes.NAME_1}`,
        suggested_area: true,
        score: 400,
        // longitude: areaCenter.coordinates[0],
        // latitude: areaCenter.coordinates[1],
        longitude: x.properties.Longitude,
        latitude: x.properties.Latitude,
        facility_name: "",
        population: x.properties.POP1,
        count: 1,
      };

      if (areaInstance) {
        // append data to existing area instance suggestion / increase the score
        let entryID = suggestions.indexOf(areaInstance);
        let entryInstance = suggestions[entryID];

        (entryInstance.score += 400),
          (entryInstance.population += x.properties.POP1);
        entryInstance.count += 1;
      } else {
        // push new data to suggestions
        suggestions.push(suggestedArea);
      }
    }
  });

  console.log(suggestions.length);

  // merge datasets
  dataset = [...suggestions];

  // sort the dataset to prioritize lower operating hours
  dataset = dataset.sort(
    (a: any, b: any) => parseFloat(b.count) - parseFloat(a.count)
  );

  // handle search query
  let searchQuery: any = req.query.search;

  if (searchQuery && searchQuery.trim() !== "") {
    const options = {
      // isCaseSensitive: false,
      // includeScore: false,
      // shouldSort: true,
      // includeMatches: false,
      // findAllMatches: false,
      // minMatchCharLength: 1,
      // location: 0,
      // threshold: 0.6,
      // distance: 100,
      // useExtendedSearch: false,
      // ignoreLocation: false,
      // ignoreFieldNorm: false,
      keys: ["municipality", "category", "type", "operating-hours", "operator"],
    };

    const fuse = new Fuse(dataset, options);
    dataset = fuse.search(searchQuery).map((x: any) => x.item);
  }

  res.send(dataset);
  return req;
};
