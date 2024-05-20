import { API } from '@/types';
import {
    DeleteApiV1AssistantsAssistantIdRequest,
    DeleteApiV1AssistantsAssistantIdResponse,
    GetApiV1AssistantsAssistantIdRequest,
    GetApiV1AssistantsAssistantIdResponse,
    PostApiV1AssistantsAssistantIdRequest,
    PostApiV1AssistantsAssistantIdResponse,
    PostApiV1AssistantsRequest,
    PostApiV1AssistantsResponse
} from '@/ytt-type/assistant';
import { request } from 'core/mz';
import { each } from 'lodash';
// 获取列表
export async function getAssistantsList(params: any) {
    return request<any>('/assistants', {
        method: 'GET',
        params,
        getResponse: true
    });
}
// 删除
export async function deleteAssistants(params: DeleteApiV1AssistantsAssistantIdRequest) {
    const { assistant_id } = params;
    return request<DeleteApiV1AssistantsAssistantIdResponse>(`/assistants/${assistant_id}`, {
        method: 'DELETE',
        params,
        getResponse: true
    });
}
// 新增
export async function addAssistants(data: PostApiV1AssistantsRequest) {
    return request<PostApiV1AssistantsResponse>('/assistants', {
        method: 'POST',
        data,
        getResponse: true
    });
}
// 查看详情
export async function assistantsDetail(params: GetApiV1AssistantsAssistantIdRequest) {
    const { assistant_id } = params;
    return request<GetApiV1AssistantsAssistantIdResponse>(`/assistants/${assistant_id}`, {
        method: 'GET',
        params,
        getResponse: true
    });
}
// 编辑确定
export async function editAssistants(data: PostApiV1AssistantsAssistantIdRequest) {
    const { assistant_id } = data;
    return request<PostApiV1AssistantsAssistantIdResponse>(`/assistants/${assistant_id}`, {
        method: 'POST',
        data,
        getResponse: true
    });
}

// 文件上传
export async function importList(body: any) {
    const formData = new FormData();
    each(body, (v: any, k: string) => {
        formData.append(k, v);
    });
    return request<any>('/files', {
        method: 'POST',
        data: formData,
        getResponse: true
    });
}

export async function getFileName(params: any) {
    return request<API.Response<any>>('/files', {
        method: 'GET',
        params
    });
}
