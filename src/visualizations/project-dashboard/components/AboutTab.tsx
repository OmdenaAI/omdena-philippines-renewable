import contributors from "./contributors.json";
import communityLinks from "./community_links.json";

const AboutTab = () => {
  return (
    <div className="research-tab px-2">
      <img
        src="/images/omdena-ph-poster.jpeg"
        className="img-fluid"
      />
      <h2 className="mt-4">Omdena Philippines Chapter</h2>
      <p>
        The project’s goal is to use Philippine satellite data in conjunction
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
