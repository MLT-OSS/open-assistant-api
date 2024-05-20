module.exports = {
    processors: [],
    plugins: [],
    extends: [
        'stylelint-config-standard',
        'stylelint-config-css-modules',
        'stylelint-config-prettier'
    ],
    rules: {
        'at-rule-name-case': 'lower',
        // 要求选择器列表的逗号之前有一个换行符
        'selector-list-comma-newline-before': 'never-multi-line',
        'block-no-empty': null,
        // 禁止低优先级的选择器出现在高优先级的选择器之后
        'no-descending-specificity': null,
        // url使用引号
        'function-url-quotes': 'always',
        'color-function-notation': 'legacy',
        // 缩进
        indentation: 4,
        'length-zero-no-unit': null,
        'alpha-value-notation': null,
        // 禁止空源
        'no-empty-source': null,
        // 禁止缺少文件末尾的换行符
        'no-missing-end-of-source-newline': null
    }
};
