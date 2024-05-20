module.exports = {
    '**/*.less': 'yarn stylelint:fix',
    '**/*.{js,jsx,ts,tsx}': 'yarn lint-staged:js',
    '**/*.{tsx,ts}': 'yarn prettier:fix'
};
