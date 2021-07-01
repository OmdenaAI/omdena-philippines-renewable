import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import MapInterface from "../components/MapInterface";
import Sidebar from "../components/Sidebar";
import { startPageLoad, stopPageLoad, Toast } from "../components/Utils";

const Index = () => {
  const [coordinates, setCoordinates] = useState(null);
  const [selectedArea, selectArea] = useState(null);

  useEffect(() => {
    startPageLoad();
    setTimeout(() => {
      stopPageLoad();
      Toast("Dashboard is Ready!");
    }, 5000);
  }, []);

  return (
    <>
      <Layout>
        <div className="grid-wrapper fade-in" />
        <Sidebar
          coordinates={coordinates}
          setCoordinates={setCoordinates}
          selectedArea={selectedArea}
        />
        <MapInterface
          coordinates={coordinates}
          setCoordinates={setCoordinates}
          selectArea={selectArea}
        />
      </Layout>
    </>
  );
};

export default Index;
