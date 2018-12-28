const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    // Disable production-specific optimizations by default
    // They can be re-enabled by running the cli with `--mode=production` or making a separate
    // webpack config for production.
    mode: 'development',

    // Entrypoints to build
    entry: {
        app: './frontend/src/app.js'
    },

    // Builded files goes into app statics
    output: {
        path: __dirname + '/django_palette/static/django-palette/js',
        filename: '[name].js'
    },

    // Modules rules
    module: {
        rules: [
            // To watch for vue components templates changes
            {
                test: /\.vue$/,
                exclude: /node_modules/,
                loader: 'vue-loader'
            },
            // To watch for every frontend source changes
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            }
        ]
    },

    // Enabled plugins
    plugins: [
        // Webpack loader for vuejs embedded rules
        new VueLoaderPlugin()
    ]
};
