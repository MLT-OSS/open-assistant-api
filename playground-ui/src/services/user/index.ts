import { API } from '@/types';
import { request } from 'core/mz';
import { LOGIN, User } from '../../types/type';

/**
 * 登录接口
 * @param body LOGIN.Form
 * @returns RequestMethodInUmi
 */
export async function login(body: LOGIN.Form) {
    return request<API.Response<User>>('/user/login', {
        method: 'POST',
        data: body
    });
}

/**
 * 退出登录
 * @return RequestMethodInUmi
 */
export async function logout() {
    return request<API.NoDataResponse>('/user/logout', {
        method: 'POST'
    });
}
/**
 * 获取用户信息基本信息接口以及权限等等
 * @param body LOGIN.Form
 * @returns RequestMethodInUmi
 */
export async function getUserInfo() {
    return request<API.Response<User>>('/user/userInfo', {
        method: 'get'
    });
}
