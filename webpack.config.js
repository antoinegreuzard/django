const glob = require('glob');
const path = require('path');

const generateEntryPoints = (pattern, basePath) => {
  return glob.sync(pattern).reduce((acc, filePath) => {
    // Obtient un chemin relatif pour le nom de l'entrée
    const entryName = path
      .relative(basePath, filePath)
      // Remplace les séparateurs de chemin par des tirets pour éviter les problèmes de chemin
      .replace(/\.js$|\.css$/, '')
      .replace(new RegExp(path.sep, 'g'), '-');

    // Utilise le chemin absolu du fichier comme valeur
    acc[entryName] = filePath;
    return acc;
  }, {});
};

// Chemins de base pour JS et CSS
const basePathJs = path.resolve(__dirname, 'app/static/app/js');

// Chemins source pour JS et CSS
const jsSourceDir = `${basePathJs}/**/*.js`;

module.exports = {
  entry: {
    ...generateEntryPoints(jsSourceDir, basePathJs),
  },
  output: {
    path: path.resolve(__dirname, 'app/static/app/bundles'),
    filename: '[name].bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
};
