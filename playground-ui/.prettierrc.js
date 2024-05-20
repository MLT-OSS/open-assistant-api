module.exports = {
    // 一行最多 120 字符
    printWidth: 120,
    // 使用 4 个空格缩进
    tabWidth: 4,
    // 不使用缩进符，而使用空格
    useTabs: false,
    // 行尾需要有分号
    semi: true,
    // 使用单引号
    singleQuote: true,
    // 末尾不需要逗号
    trailingComma: 'none',
    // 大括号内的首尾需要空格
    bracketSpacing: true,
    // jsx 标签的反尖括号需要换行
    bracketSameLine: true,
    // 箭头函数，只有一个参数的时候，也需要括号
    arrowParens: 'always',
    // 每个文件格式化的范围是文件的全部内容
    rangeStart: 0,
    rangeEnd: Infinity,
    // 不需要写文件开头的 @prettier
    requirePragma: false,
    // 不需要自动在文件开头插入 @prettier
    insertPragma: false,
    // 使用默认的折行标准
    proseWrap: 'preserve',
    // 根据显示样式决定 html 要不要折行 ignore
    htmlWhitespaceSensitivity: 'strict',
    // 换行符使用 lf
    endOfLine: 'lf',

    parser: 'typescript',

    overrides: [
        {
            files: ['*.json'],
            options: {
                parser: 'json',
                tabWidth: 2
            }
        },
        {
            files: '*.{css,sass,scss,less}',
            options: {
                parser: 'css',
                tabWidth: 4
            }
        },
        {
            files: '*.{ts,tsx}',
            options: {
                parser: 'typescript'
            }
        }
    ]
};
