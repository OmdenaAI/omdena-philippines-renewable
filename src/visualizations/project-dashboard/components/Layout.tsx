import Head from "next/head";

const Layout = (props: any) => {
  return (
    <>
      <Head>
        <link rel="icon" href="/images/omdena-ph.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#000000" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="Sol Dashboard" content="Web application" />
        <title>Potential Solar Powerplant Sites | Omdena Philippines</title>
        <link
          href="https://demos.creative-tim.com/argon-dashboard/assets/css/argon.min.css?v=1.2.0"
          rel="stylesheet"
        />
        <link
          rel="stylesheet"
          href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css"
        />
      </Head>
      {props.children}
    </>
  );
};

export default Layout;
