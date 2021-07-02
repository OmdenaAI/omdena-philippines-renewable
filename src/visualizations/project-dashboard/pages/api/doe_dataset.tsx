import type { NextApiRequest, NextApiResponse } from "next";
import { guid } from "../../components/Utils";
import DOE_dataset from "./project_simoy_doe_dataset.json";

export default (req: NextApiRequest, res: NextApiResponse) => {
  // add unique id to dataset
  let dataset: any = [...DOE_dataset];
  dataset.forEach((x: any) => {
    x.id = guid();
  });
  res.send(dataset);
  return req;
};
