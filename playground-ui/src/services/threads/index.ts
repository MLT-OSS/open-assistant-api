import { API } from '@/types';
import { request } from 'core/mz';

/**
 * -----------threads----------
 */

// create thread
export async function createThreads(data: any) {
    return request<API.NoDataResponse>(`/threads`, {
        method: 'post',
        data,
        getResponse: true
    });
}
// get thread
export async function threads(thread_id: string, params: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}`, {
        method: 'get',
        params
    });
}
// modify thread
export async function modifyThreads(thread_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}`, {
        method: 'post',
        data
    });
}
// delete thread
export async function deleteThreads(thread_id: string) {
    return request<API.NoDataResponse>(`/threads/${thread_id}`, {
        method: 'delete'
    });
}

/**
 * -----------messages----------
 */
// list messages
export async function listMessages(thread_id: string, params: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages`, {
        method: 'get',
        params
    });
}

// create messages
export async function createMessages(thread_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages`, {
        method: 'post',
        data,
        getResponse: true
    });
}
// get message
export async function getMessages(thread_id: string, message_id: string) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages/${message_id}`, {
        method: 'get'
    });
}

// modify message
export async function modifyMessages(thread_id: string, message_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages/${message_id}`, {
        method: 'post',
        data
    });
}

// list message Files
export async function listMessageFiles(thread_id: string, message_id: string, params: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages/${message_id}/files`, {
        method: 'get',
        params
    });
}

// get message File
export async function getMessageFile(thread_id: string, message_id: string, file_id: string) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/messages/${message_id}/files/${file_id}`, {
        method: 'get'
    });
}

/**
 * -----------runs----------
 */

// create thread and run
export async function createThreadAndRun(data: any) {
    return request<API.NoDataResponse>(`/threads/runs`, {
        method: 'post',
        data
    });
}

// list runs
export async function runsList(thread_id: string, params: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs`, {
        method: 'GET',
        params
    });
}

// create run
export async function createRuns(thread_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs`, {
        method: 'post',
        data,
        getResponse: true
    });
}

// get run
export async function getRuns(thread_id: string, run_id: string) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}`, {
        method: 'get'
    });
}
// modify run
export async function modifyRuns(thread_id: string, run_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}`, {
        method: 'post',
        data
    });
}

// cancel run
export async function cancelRuns(thread_id: string, run_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}/cancel`, {
        method: 'post',
        data
    });
}
// list steps run
export async function getRunsSteps(thread_id: string, run_id: string, params: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}/steps`, {
        method: 'get',
        params
    });
}
// get run step
export async function getRunStepById(thread_id: string, run_id: string, step_id: string) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}/steps/${step_id}`, {
        method: 'get'
    });
}

// submit tool ouputs to run
export async function submitToolOutputsToRun(thread_id: string, run_id: string, data: any) {
    return request<API.NoDataResponse>(`/threads/${thread_id}/runs/${run_id}/submit_tool_outputs`, {
        method: 'post',
        data
    });
}
