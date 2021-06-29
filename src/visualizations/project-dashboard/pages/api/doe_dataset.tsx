import type { NextApiRequest, NextApiResponse } from "next";
import DOE_dataset from "./project_simoy_doe_dataset.json";

export default (req: NextApiRequest, res: NextApiResponse) => {
  res.send(DOE_dataset);
};
