export default {
    dev: {
        '/api': {
            target: 'http://api:8086',
            changeOrigin: true,
            // pathRewrite: { '^/api': '' },
            secure: false
        }
    }
};
