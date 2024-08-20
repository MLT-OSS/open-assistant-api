/*
 * 网络请求异常处理程序
 */
import { RequestError } from '@@/plugin-request/request';
import { notification } from 'antd';
import { ArgsProps } from 'antd/lib/notification/index';

/**
 * @description: 业务异常码 and http状态码
 * @param {number}
 */
const codeMessage: {
    [key: number]: string;
} = {
    '200': '服务器成功返回请求的数据',
    '401': '认证失败。',
    '403': '用户得到授权，但是访问是被禁止的。',
    '500': '服务器发生错误，请检查服务器。',
    '502': '网关错误。',
    '503': '服务不可用，服务器暂时过载或维护。',
    '504': '网关超时。',
    '-1001': '导入失败'
};

interface error {
    name: string;
    data: any;
    type: string;
    response: {
        code: any;
        status: any;
        msg: string;
    };
}
const notificationMap = new Map();
/**
 * 推送消息
 * @param option ArgsProps
 */
function pushNotification(option: ArgsProps) {
    notificationMap.set(option.message, option);
    setTimeout(() => {
        const key = notificationMap.keys().next().value;
        const val = notificationMap.get(key);
        if (val) {
            notificationMap.delete(key);
            notification.error(val);
        }
    }, 1000);
}
/**
 * 异常处理程序
 */
const errorHandler = (error: RequestError | any, opts: any) => {
    if (opts?.skipErrorHandler) throw error;
    if (error.name === 'BizError') {
        pushNotification({
            message: error.message || '接口错误！'
        });
    } else if (error.response) {
        const errorText = codeMessage[error.response.status];
        pushNotification({
            message: errorText || '接口错误！'
        });
    } else if (error.request) {
        pushNotification({
            message: '接口超时！'
        });
    } else {
        pushNotification({
            message: '网络异常'
        });
    }
    throw error;
};

export default errorHandler;
