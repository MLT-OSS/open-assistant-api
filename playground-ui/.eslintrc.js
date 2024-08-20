module.exports = {
    extends: ['eslint-config-mlt'],
    env: {
        browser: true
    },
    plugins: ['unicorn'],
    globals: {
        // 这里填入你的项目需要的全局变量
        // 这里值为 false 表示这个全局变量不允许被重新赋值，比如：
        // jQuery: false,
        // $: false
    },
    settings: {
        react: {
            version: 'detect'
        }
    },
    rules: {
        'no-undef': 0,
        'unicorn/filename-case': [
            'error',
            {
                case: 'kebabCase',
                ignore: ['[a-z]{2}-[A-Z]{2}.ts', '^\\[\\S*\\].tsx']
            }
        ]
    }
};
