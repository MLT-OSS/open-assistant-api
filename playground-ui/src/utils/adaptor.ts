import type { AxiosResponse } from '@@/plugin-request/request';
interface ResponseStructure {
    success: boolean;
    data: any;
    code?: number;
    msg?: string;
    showType?: number;
}
export const errorThrower = (res: ResponseStructure) => {
    const { success, data, code: errorCode, msg: errorMessage, showType } = res;
    if (!success) {
        const error: any = new Error(errorMessage);
        error.name = 'BizError';
        error.info = { errorCode, errorMessage, showType, data };
        throw error; // 抛出自制的错误
    }
};
/**
 * 数据适配器, 团队根据自己的情况来做适配
 *
 */
export default (response: AxiosResponse) => {
    if (response.data instanceof Blob) {
        return response;
    }
    try {
        const code = String(response?.data?.code || response?.status);
        if (code === '0' || code === '200') {
            response.data['success'] = true;
        } else {
            response.data['success'] = false;
        }
        return response;
    } catch (error) {
        response.data['success'] = false;
        return response;
    }
};
