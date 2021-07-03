import type { NextApiRequest, NextApiResponse } from "next";
import { guid } from "../../components/Utils";
import DOE_dataset from "./project_simoy_doe_dataset.json";

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];
  dataset.forEach((x: any) => {
    x.id = guid();
    if (x.connection_type === "Off-Grid") {
      x.suggested_area = true;
    }
  });

  // sort the dataset to prioritize lower operating hours
  dataset = dataset.sort(
    (a: any, b: any) =>
      parseFloat(a.operating_hours) - parseFloat(b.operating_hours)
  );

  res.send(dataset);
  return req;
};
