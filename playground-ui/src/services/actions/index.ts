import { request } from 'core/mz';

// 获取列表
export async function getList(params: any) {
    return request('/actions', {
        method: 'GET',
        params,
        getResponse: true
    });
}

// 创建actions
export async function create(data: any) {
    return request('/actions', {
        method: 'POST',
        data
    });
}

// 获取actions详情
export async function get(id: string) {
    return request(`/actions/${id}`, {
        method: 'GET',
        getResponse: true
    });
}

// 删除actions
export async function del(id: string) {
    return request(`/actions/${id}`, {
        method: 'DELETE',
        getResponse: true
    });
}

// 更新actions
export async function update(id: string, data: any) {
    return request(`/actions/${id}`, {
        method: 'POST',
        data
    });
}

// api run action
export async function runAction(id: string) {
    return request(`/actions/${id}/run`, {
        method: 'POST'
    });
}
