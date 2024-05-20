/*
 * @Author: 魏娇莹
 * @Date: 2023-12-25 14:26:00
 * @LastEditors: 魏娇莹
 * @LastEditTime: 2023-12-26 15:44:38
 * @Description:
 */
export default {
    dev: {
        '/api': {
            target: 'https://localhost:8086',
            changeOrigin: true,
            // pathRewrite: { '^/api': '' },
            secure: false
        }
    }
};
