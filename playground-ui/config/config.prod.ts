export default {
    mfsu: false,
    devtool: false,
    define: {
         APIURL: '/api/v1',
        'process.env.UMI_ENV': process.env.UMI_ENV,
    }
};
