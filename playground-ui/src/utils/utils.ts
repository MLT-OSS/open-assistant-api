/*
 *
 */
export const isJson = (str: string) => {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
};

export const isNil = (value: any) => value === null || value === undefined;
