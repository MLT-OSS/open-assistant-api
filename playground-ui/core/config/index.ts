import { resolve } from 'path';
import proxy from '../../config/proxy';
import routes from '../../config/routes';

const { UMI_ENV } = process.env;

export default function MzConfig(config: any) {
    const defaultConfig = {
        hash: true,
        locale: {
            default: 'zh-CN',
            antd: true,
            // default true, when it is true, will use `navigator.language` overwrite default
            baseNavigator: true,
            baseSeparator: '-'
        },
        alias: {
            core: resolve(__dirname, '../')
        },
        routes: routes,
        targets: {},
        manifest: {
            basePath: '/'
        },
        ignoreMomentLocale: true,
        proxy: (proxy as any)[UMI_ENV || 'dev'],
        mfsu: {},
        cssLoaderModules: {
            // 配置驼峰式使用
            exportLocalsConvention: 'camelCase'
        },
        title: 'umi'
    };

    return { ...defaultConfig, ...config };
}
