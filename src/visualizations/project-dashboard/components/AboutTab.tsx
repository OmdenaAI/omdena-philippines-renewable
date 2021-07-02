import contributors from "./contributors.json";
import communityLinks from "./community_links.json";

const AboutTab = () => {
  return (
    <div className="research-tab px-2">
      <img
        src="https://media-exp1.licdn.com/dms/image/C5622AQHu7Y0Nx0RR2A/feedshare-shrink_1280/0/1622549311322?e=1628121600&v=beta&t=fEieL9q7Sl3ExmiHg4BYIE4pm6ezYs14PzdreCwtecA"
        className="img-fluid"
      />
      <h2 className="mt-4">Omdena Philippines Chapter</h2>
      <p>
        Increasing Renewable Energy Access in Philippines through AI This
        initiative’s goal is to use Philippine satellite data in conjunction
        with other relevant dataset to identify sites that are most suitable for
        solar panel installation as a greener energy source through machine
        learning and coverage analysis.
      </p>

      <h2>Contributors</h2>
      <p>Meet the people who made this project possible.</p>

      <div className="contributors">
        {contributors.map((contributor: any, index: number) => {
          return (
            <a href={contributor.url} target="_blank">
              <div className="contributor" key={index}>
                <img src={contributor.profileImage} className="avatar" />
                <div className="info">
                  <span className="name">{contributor.name}</span>
                  <span className="info">{contributor.info}</span>
                </div>
              </div>
            </a>
          );
        })}
      </div>

      <br />

      <h2>Join the Community</h2>
      <p>Learn more about Omdena and Join the community!</p>

      <div className="contributors">
        {communityLinks.map((contributor: any, index: number) => {
          return (
            <a href={contributor.url} target="_blank">
              <div className="contributor" key={index}>
                <img src={contributor.profileImage} className="avatar" />
                <div className="info">
                  <span className="name">{contributor.name}</span>
                  <span className="info">{contributor.info}</span>
                </div>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
};

export default AboutTab;
