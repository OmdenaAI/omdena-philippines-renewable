import type { NextApiRequest, NextApiResponse } from "next";
import DOE_dataset from "./doe_v1.json";
import correlated_data from "./correlated_data.json";
import Fuse from "fuse.js";

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];

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
