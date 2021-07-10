import type { NextApiRequest, NextApiResponse } from "next";
// import { guid } from "../../components/Utils";
import DOE_dataset from "./doe_v1.json";
import Fuse from "fuse.js";

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];
  // dataset.forEach((x: any) => {
  // if (x.connection_type === "Off-Grid") {
  //   x.suggested_area = true;
  // }
  // make sure to only suggested areas with power stations that
  // operate less thatn 24 hours
  // if (x.operating_hours < 24) {
  //   x.suggested_area = true;
  // } else {
  //   x.suggested_area = false;
  // }

  // });

  // sort the dataset to prioritize lower operating hours
  dataset = dataset.sort(
    (a: any, b: any) =>
      parseFloat(a.operating_hours) - parseFloat(b.operating_hours)
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
