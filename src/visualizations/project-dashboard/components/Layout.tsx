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
        <meta
      property="og:title"
      content="Potential Solar Powerplant Sites in the Philippines | Omdena Philippines"
    />
    <meta property="og:image" content="https://omdenaph-solar.vercel.app/images/splash.png" />
    <meta property="og:url" content="https://omdenaph-solar.vercel.app/" />
    <meta
      property="og:description"
      content="Finding the best places to build Solar power stations in the Philipppines using Data Science"
    />

    <link rel="apple-touch-icon" href="%PUBLIC_URL%/hydra.png" />
        <title>Potential Solar Powerplant Sites | Omdena Philippines</title>
        <link
          href="https://demos.creative-tim.com/argon-dashboard/assets/css/argon.min.css?v=1.2.0"
          rel="stylesheet"
        />
        <link
          rel="stylesheet"
          href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css"
        />

        <script async src="https://www.googletagmanager.com/gtag/js?id=G-QLS9Q801BN"></script>
        <script dangerouslySetInnerHTML={{__html: `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-QLS9Q801BN');
        `}}>
        </script>
      </Head>
      {props.children}
    </>
  );
};

export default Layout;
