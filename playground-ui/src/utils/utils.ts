/*
 *
 */
export const isJson = (str: string) => {
    try {
        const result = JSON.parse(str);
        const type = Object.prototype.toString.call(result);
        return type === '[object Object]' || type === '[object Array]';
    } catch (e) {
        return false;
    }
};

export const isNil = (value: any) => value === null || value === undefined;
