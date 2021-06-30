import { useEffect } from "react";

const SiteDetails = (props: any) => {
  const data = props.data;

  useEffect(() => {
    let sidebarContainer: any = document.querySelector(".sidebar");
    setTimeout(() => {
      sidebarContainer.scroll({ top: 0, behavior: "smooth" });
    }, 200);
  }, []);

  return (
    <>
      <div className="cover-card fade-in dl-2 flex-column">
        <h2 className="mt-auto text-white mb--1">{data.facility_name}</h2>
        <small className="text-white">{data.municipality}</small>
      </div>
      <div className="card p-2 px-3">
        <p>{data.municipality}</p>
      </div>

      <div className="container-fluid fade-in-bottom table-container">
        <div className="row">
          <div className="col">
            <div className="card border">
              <div className="card-header  table-header">
                <h4 className="mb-0">
                  <i className="la la-user" /> Site Details
                </h4>
              </div>
              <div className="table-responsive">
                <table className="table align-items-center table-flush">
                  <tbody className="list">
                    {data &&
                      Object.keys(data).map((x: any, index: number) => {
                        return (
                          <tr className={`${index === 0 ? "est-head" : ""}`}>
                            <td>
                              <span>{x}</span>
                            </td>
                            <td>
                              <span>-</span>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SiteDetails;
