var webpack = require('webpack');

module.exports = {
    entry:[
        './src/index.jsx'
    ],
    output: {
        path: __dirname + '/dist/',
        publicPath: "/dist/",
        filename: 'bundle.js'
    },
    debug: true,
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        loaders: [
            {
                test: /.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: ['es2015', 'react']
                }
            },
            {
                test: /\.css$/, // Only .css files
                loader: 'style!css' // Run both loaders
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
        new webpack.DefinePlugin({
            "__DEV__": process.env.DEV || false
        })
    ]
};
