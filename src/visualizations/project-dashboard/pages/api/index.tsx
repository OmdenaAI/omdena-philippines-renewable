import type { NextApiRequest, NextApiResponse } from "next";

const API_INFO = {
  version: "v1",
  name: "Omeda Philippines API",
};

export default (req: NextApiRequest, res: NextApiResponse) => {
  res.send(API_INFO);
  return req;
};
