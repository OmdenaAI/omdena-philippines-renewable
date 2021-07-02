const MarkerLegends = () => {
  const MarkerLabels: any = [
    {
      name: "Suggested Areas",
      classification: "Off-Grid",
    },
    {
      name: "Solar Power Station",
      classification: "Solar",
    },
    {
      name: "Hydroelectric Powerplant",
      classification: "Hydroelectric",
    },
    {
      name: "Geothermal Powerplant",
      classification: "Geothermal",
    },
    {
      name: "Wind Power Station",
      classification: "Wind",
    },
    {
      name: "Oil Power Station",
      classification: "Oil-Based",
    },
    {
      name: "Natural Gas Powerplant",
      classification: "NaturalGas",
    },
    {
      name: "Biomass Powerplant",
      classification: "Biomass",
    },
    {
      name: "Coal-fired Powerstation",
      classification: "Coal",
    },
  ];

  return (
    <div className="marker-legends fade-in-bottom">
      <small>
        <i className="la la-map-marker text-info" /> Marker Labels
      </small>

      <ul className="pt-2">
        {MarkerLabels.map((item: any, index: number) => {
          return (
            <li key={index}>
              <div className={`label-icon ${item.classification}`} />

              {item.name}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default MarkerLegends;
