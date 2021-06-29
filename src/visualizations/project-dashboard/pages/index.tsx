import { useEffect } from "react";
import Layout from "../components/Layout";
import Sidebar from "../components/Sidebar";
import { startPageLoad, stopPageLoad, Toast } from "../components/Utils";

const Index = () => {
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
        <Sidebar />
      </Layout>
    </>
  );
};

export default Index;
