import type { NextApiRequest, NextApiResponse } from "next";
import DOE_dataset from "./doe_v1.json";
import correlated_data from "./correlated_data.json";
import Fuse from "fuse.js";

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];

  // add identifiers to power sources for analytics
  // this is used to differentiate powers sources from suggested areas
  dataset.forEach((x: any) => {
    x.power_station = true;
  });

  // merge datasets
  dataset = [...dataset, ...correlated_data];

  // sort the dataset to prioritize lower operating hours
  dataset = dataset.sort(
    (a: any, b: any) => parseFloat(a.response) - parseFloat(b.response)
  );

  // handle search query
  let searchQuery: any = req.query.search;

  if (searchQuery && searchQuery.trim() !== "") {
    const options = {
      keys: ["municipality", "category", "type", "operating-hours", "operator"],
    };

    const fuse = new Fuse(dataset, options);
    dataset = fuse.search(searchQuery).map((x: any) => x.item);
  }

  res.send(dataset);
  return req;
};
