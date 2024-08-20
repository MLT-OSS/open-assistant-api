import { defineConfig } from 'yapi-to-typescript';

interface IConfig {
    ids: number[]; // 分类 ids，可以将多个分类中的接口信息生成到同一个 ts 文件中
    name: string; // 输出的 ts 文件存储模块文件夹名称，对应的文件夹名称为 src/ytt-type/[name]
    token?: string; // 项目 Token, 如果不填就用公共的 Token
}

const TOKEN = 'xxx';

const config: IConfig[] = [
    { ids: [11474], name: 'assistant' },
    { ids: [11476], name: 'threads' },
    { ids: [11478], name: 'messages' },
    { ids: [11480], name: 'runs' },
    { ids: [11482], name: 'files' }
];

const createCategories = function (ids: number[]) {
    return ids.map((id) => ({
        id,
        // 自定义ts中interface名称生成规则
        getRequestFunctionName(interfaceInfo: any, changeCase: any) {
            // path肯定是唯一的
            const list = interfaceInfo.path.split('/') as string[];
            // 添加method用于区分post，get，put请求可能path相同
            const firstWord = list[0].toLowerCase();
            if (!/^get|^post|^put|^delete/.test(firstWord)) {
                list.unshift(interfaceInfo.method);
            }
            return changeCase.camelCase(list.join(' '));
        }
    }));
};

export default defineConfig(
    config.map((item) => ({
        // 1. 此处配置yapi的访问地址
        serverUrl: 'https://yapi.com',
        typesOnly: false,
        target: 'typescript',
        reactHooks: {
            enabled: false
        },
        prodEnvName: 'production',
        outputFilePath: `src/ytt-type/${item.name}/index.ts`,
        requestFunctionFilePath: `src/ytt-type/${item.name}/request.ts`,
        // dataKey: 'data',
        projects: [
            {
                // 2. 此处配置yapi项目的访问token
                token: item.token ?? TOKEN,
                categories: createCategories(item.ids)
            }
        ]
    }))
);
