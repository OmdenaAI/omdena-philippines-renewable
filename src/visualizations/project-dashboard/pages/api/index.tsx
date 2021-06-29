import type { NextApiRequest, NextApiResponse } from "next";

const API_INFO = {
  version: "v1",
  name: "Beta API",
};

export default (req: NextApiRequest, res: NextApiResponse) => {
  console.log(req);
  res.send(API_INFO);
};
