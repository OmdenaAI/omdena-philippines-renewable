import links from "./research_links.json";

const ReasearchTab = () => {
  return (
    <div className="research-tab px-1">
      <div className="research-cover-card fade-in">
        <h1 className="mt-auto text-white mb--1">Research</h1>
      </div>
      <p className="mt--2">
        Below is a list of articles and resources that will help you understand
        how the project was built.
      </p>

      <div className="contributors mt-4">
        {links.map((contributor: any, index: number) => {
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

export default ReasearchTab;
