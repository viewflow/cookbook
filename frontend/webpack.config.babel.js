import path from 'path';

const BABEL_LOADER_CONFIG = {
  test: /\.js$/,
  exclude: [path.resolve(__dirname, './node_modules')],
  loader: 'babel-loader',
};

const JAVASCRIPT_CONFIG = {
  entry: {
    'my-components': './components/my-components.js',
  },

  output: {
    filename: 'js/[name].min.js',
    path: path.resolve(__dirname, './static/'),
  },

  devtool: 'source-map',

  module: {
    rules: [
      BABEL_LOADER_CONFIG,
    ],
  },
};


export default [
  JAVASCRIPT_CONFIG,
];
