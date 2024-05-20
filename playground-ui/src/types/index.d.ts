// @ts-ignore
export interface InitialState {
    userId: string;
    userName: string;
    permissions?: any; // 权限
}

export declare namespace API {
    interface Response<D> {
        code: number;
        msg: string;
        data: D;
    }

    interface NoDataResponse {
        code: number;
        msg: string;
    }
}

declare global {
    const APIURL: string;
}
