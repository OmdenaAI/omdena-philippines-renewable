import Skeleton, { SkeletonTheme } from "react-loading-skeleton";

const LoadingSkeleton = () => {
  let RowCount = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9];
  return (
    <>
      {RowCount.map((skeletonCard: any) => {
        return (
          <SkeletonTheme
            color="#e7e7e7"
            highlightColor="#f7f7f7"
            key={skeletonCard}
          >
            <div className="card-item">
              <div className="card-item-content">
                <div className="score-card">
                  <span>
                    <i className="la la-sun" />
                  </span>
                </div>

                <div className="card-info">
                  <span>
                    <Skeleton count={1} />
                  </span>
                  <div className="tag-row mt-1">
                    <Skeleton
                      count={1}
                      style={{ width: "50px", marginRight: "10px" }}
                    />
                    <Skeleton count={1} style={{ width: "50px" }} />
                  </div>
                </div>
              </div>
              <Skeleton count={1} style={{ width: "50px" }} />
            </div>
          </SkeletonTheme>
        );
      })}
    </>
  );
};

export default LoadingSkeleton;
