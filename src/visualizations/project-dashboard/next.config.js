const withSass = require("@zeit/next-sass");
const withCSS = require("@zeit/next-css");
const withFonts = require("next-fonts");

module.exports = withFonts(
  withCSS(
    withSass({
      enableSvg: true,
      webpack: function (config) {
        config.module.rules.push({
          test: /\.(eot|woff|woff2|ttf|svg|png|jpg|gif)$/,
          use: {
            loader: "url-loader",
            options: {
              limit: 100000,
              name: "[name].[ext]",
            },
          },
        });
        return config;
      },
      env: {
        PRODUCTION: process.env.PRODUCTION,
      },
    })
  )
);
