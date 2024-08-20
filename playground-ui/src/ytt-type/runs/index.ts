/* prettier-ignore-start */
/* tslint:disable */
/* eslint-disable */

/* 该文件由 yapi-to-typescript 自动生成，请勿直接修改！！！ */

// @ts-ignore
// prettier-ignore
// @ts-ignore
// prettier-ignore
import type { RequestConfig,RequestFunctionRestArgs } from 'yapi-to-typescript';
import { Method, prepare, QueryStringArrayFormat, RequestBodyType, ResponseBodyType } from 'yapi-to-typescript';
// @ts-ignore
import request from './request';

type UserRequestRestArgs = RequestFunctionRestArgs<typeof request>;

// Request: 目前 React Hooks 功能有用到
export type Request<
    TRequestData,
    TRequestConfig extends RequestConfig,
    TRequestResult
> = (TRequestConfig['requestDataOptional'] extends true
    ? (requestData?: TRequestData, ...args: RequestFunctionRestArgs<typeof request>) => TRequestResult
    : (requestData: TRequestData, ...args: RequestFunctionRestArgs<typeof request>) => TRequestResult) & {
    requestConfig: TRequestConfig;
};

const mockUrl_3_0_0_0 = 'https://yapi.com/mock/926' as any;
const devUrl_3_0_0_0 = '' as any;
const prodUrl_3_0_0_0 = '' as any;
const dataKey_3_0_0_0 = undefined as any;

/**
 * 接口 [List Runs↗](https://yapi.com/project/926/interface/api/70380) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
    thread_id: string;
}

/**
 * 接口 [List Runs↗](https://yapi.com/project/926/interface/api/70380) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsResponse {
    object?: string;
    data?: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        instructions?: string;
        model?: string;
        status?: string;
        assistant_id: string;
        thread_id?: string;
        object?: string;
        file_ids?: unknown[];
        metadata_?: {};
        last_error?: {};
        required_action?: {};
        tools?: unknown[];
        started_at?: string;
        completed_at?: string;
        cancelled_at?: string;
        expires_at?: string;
        failed_at?: string;
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Runs↗](https://yapi.com/project/926/interface/api/70380) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdRunsRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs',
        undefined,
        'thread_id',
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Runs↗](https://yapi.com/project/926/interface/api/70380) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdRunsRequestConfig: GetApiV1ThreadsThreadIdRunsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_3_0_0_0,
    devUrl: devUrl_3_0_0_0,
    prodUrl: prodUrl_3_0_0_0,
    path: '/api/v1/threads/{thread_id}/runs',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_3_0_0_0,
    paramNames: ['thread_id'],
    queryNames: ['limit', 'order', 'after', 'before'],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1ThreadsThreadIdRuns',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [List Runs↗](https://yapi.com/project/926/interface/api/70380) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdRuns = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdRunsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdRunsResponse>(
        prepare(getApiV1ThreadsThreadIdRunsRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdRuns.requestConfig = getApiV1ThreadsThreadIdRunsRequestConfig;

/**
 * 接口 [Create Run↗](https://yapi.com/project/926/interface/api/70386) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRequest {
    assistant_id: string;
    status?: string;
    instructions?: string;
    model?: string;
    file_ids?: unknown[];
    metadata?: {};
    tools?: unknown[];
    thread_id: string;
}

/**
 * 接口 [Create Run↗](https://yapi.com/project/926/interface/api/70386) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Create Run↗](https://yapi.com/project/926/interface/api/70386) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdRunsRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs',
        undefined,
        'thread_id',
        string,
        false
    >
>;

/**
 * 接口 [Create Run↗](https://yapi.com/project/926/interface/api/70386) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdRunsRequestConfig: PostApiV1ThreadsThreadIdRunsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_3_0_0_0,
    devUrl: devUrl_3_0_0_0,
    prodUrl: prodUrl_3_0_0_0,
    path: '/api/v1/threads/{thread_id}/runs',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_3_0_0_0,
    paramNames: ['thread_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1ThreadsThreadIdRuns',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create Run↗](https://yapi.com/project/926/interface/api/70386) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdRuns = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdRunsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdRunsResponse>(
        prepare(postApiV1ThreadsThreadIdRunsRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdRuns.requestConfig = postApiV1ThreadsThreadIdRunsRequestConfig;

/**
 * 接口 [Get Run↗](https://yapi.com/project/926/interface/api/70392) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdRequest {
    thread_id: string;
    run_id: string;
}

/**
 * 接口 [Get Run↗](https://yapi.com/project/926/interface/api/70392) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Get Run↗](https://yapi.com/project/926/interface/api/70392) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdRunsRunIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}',
        undefined,
        'thread_id' | 'run_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Run↗](https://yapi.com/project/926/interface/api/70392) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdRunsRunIdRequestConfig: GetApiV1ThreadsThreadIdRunsRunIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_3_0_0_0,
    devUrl: devUrl_3_0_0_0,
    prodUrl: prodUrl_3_0_0_0,
    path: '/api/v1/threads/{thread_id}/runs/{run_id}',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_3_0_0_0,
    paramNames: ['thread_id', 'run_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1ThreadsThreadIdRunsRunId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Get Run↗](https://yapi.com/project/926/interface/api/70392) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdRunsRunId = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdRunsRunIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdRunsRunIdResponse>(
        prepare(getApiV1ThreadsThreadIdRunsRunIdRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdRunsRunId.requestConfig = getApiV1ThreadsThreadIdRunsRunIdRequestConfig;

/**
 * 接口 [Modify Run↗](https://yapi.com/project/926/interface/api/70398) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdRequest {
    tools?: unknown[];
    metadata?: {};
    thread_id: string;
    run_id: string;
}

/**
 * 接口 [Modify Run↗](https://yapi.com/project/926/interface/api/70398) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Modify Run↗](https://yapi.com/project/926/interface/api/70398) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdRunsRunIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}',
        undefined,
        'thread_id' | 'run_id',
        string,
        false
    >
>;

/**
 * 接口 [Modify Run↗](https://yapi.com/project/926/interface/api/70398) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdRunsRunIdRequestConfig: PostApiV1ThreadsThreadIdRunsRunIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_3_0_0_0,
    devUrl: devUrl_3_0_0_0,
    prodUrl: prodUrl_3_0_0_0,
    path: '/api/v1/threads/{thread_id}/runs/{run_id}',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_3_0_0_0,
    paramNames: ['thread_id', 'run_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1ThreadsThreadIdRunsRunId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Modify Run↗](https://yapi.com/project/926/interface/api/70398) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdRunsRunId = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdRunsRunIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdRunsRunIdResponse>(
        prepare(postApiV1ThreadsThreadIdRunsRunIdRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdRunsRunId.requestConfig = postApiV1ThreadsThreadIdRunsRunIdRequestConfig;

/**
 * 接口 [Cancel Run↗](https://yapi.com/project/926/interface/api/70404) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/cancel`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdCancelRequest {
    thread_id: string;
    run_id: string;
}

/**
 * 接口 [Cancel Run↗](https://yapi.com/project/926/interface/api/70404) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/cancel`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdCancelResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Cancel Run↗](https://yapi.com/project/926/interface/api/70404) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/cancel`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdRunsRunIdCancelRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}/cancel',
        undefined,
        'thread_id' | 'run_id',
        string,
        false
    >
>;

/**
 * 接口 [Cancel Run↗](https://yapi.com/project/926/interface/api/70404) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/cancel`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdRunsRunIdCancelRequestConfig: PostApiV1ThreadsThreadIdRunsRunIdCancelRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_3_0_0_0,
        devUrl: devUrl_3_0_0_0,
        prodUrl: prodUrl_3_0_0_0,
        path: '/api/v1/threads/{thread_id}/runs/{run_id}/cancel',
        method: Method.POST,
        requestHeaders: {},
        requestBodyType: RequestBodyType.raw,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_3_0_0_0,
        paramNames: ['thread_id', 'run_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'postApiV1ThreadsThreadIdRunsRunIdCancel',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Cancel Run↗](https://yapi.com/project/926/interface/api/70404) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/cancel`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdRunsRunIdCancel = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdRunsRunIdCancelRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdRunsRunIdCancelResponse>(
        prepare(postApiV1ThreadsThreadIdRunsRunIdCancelRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdRunsRunIdCancel.requestConfig = postApiV1ThreadsThreadIdRunsRunIdCancelRequestConfig;

/**
 * 接口 [List Run Steps↗](https://yapi.com/project/926/interface/api/70410) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdStepsRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
    thread_id: string;
    run_id: string;
}

/**
 * 接口 [List Run Steps↗](https://yapi.com/project/926/interface/api/70410) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdStepsResponse {
    object?: string;
    data?: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        status: string;
        type: string;
        assistant_id: string;
        thread_id: string;
        run_id: string;
        object?: string;
        metadata_?: {};
        last_error?: {};
        step_details?: {};
        completed_at?: string;
        cancelled_at?: string;
        expires_at?: string;
        failed_at?: string;
        message_id?: string;
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Run Steps↗](https://yapi.com/project/926/interface/api/70410) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdRunsRunIdStepsRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}/steps',
        undefined,
        'thread_id' | 'run_id',
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Run Steps↗](https://yapi.com/project/926/interface/api/70410) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdRunsRunIdStepsRequestConfig: GetApiV1ThreadsThreadIdRunsRunIdStepsRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_3_0_0_0,
        devUrl: devUrl_3_0_0_0,
        prodUrl: prodUrl_3_0_0_0,
        path: '/api/v1/threads/{thread_id}/runs/{run_id}/steps',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_3_0_0_0,
        paramNames: ['thread_id', 'run_id'],
        queryNames: ['limit', 'order', 'after', 'before'],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1ThreadsThreadIdRunsRunIdSteps',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [List Run Steps↗](https://yapi.com/project/926/interface/api/70410) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdRunsRunIdSteps = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdRunsRunIdStepsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdRunsRunIdStepsResponse>(
        prepare(getApiV1ThreadsThreadIdRunsRunIdStepsRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdRunsRunIdSteps.requestConfig = getApiV1ThreadsThreadIdRunsRunIdStepsRequestConfig;

/**
 * 接口 [Get Run Step↗](https://yapi.com/project/926/interface/api/70416) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequest {
    thread_id: string;
    run_id: string;
    step_id: string;
}

/**
 * 接口 [Get Run Step↗](https://yapi.com/project/926/interface/api/70416) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    status: string;
    type: string;
    assistant_id: string;
    thread_id: string;
    run_id: string;
    object?: string;
    metadata_?: {};
    last_error?: {};
    step_details?: {};
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
    message_id?: string;
}

/**
 * 接口 [Get Run Step↗](https://yapi.com/project/926/interface/api/70416) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}',
        undefined,
        'thread_id' | 'run_id' | 'step_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Run Step↗](https://yapi.com/project/926/interface/api/70416) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequestConfig: GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_3_0_0_0,
        devUrl: devUrl_3_0_0_0,
        prodUrl: prodUrl_3_0_0_0,
        path: '/api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_3_0_0_0,
        paramNames: ['thread_id', 'run_id', 'step_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1ThreadsThreadIdRunsRunIdStepsStepId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Get Run Step↗](https://yapi.com/project/926/interface/api/70416) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdRunsRunIdStepsStepId = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdRunsRunIdStepsStepIdResponse>(
        prepare(getApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdRunsRunIdStepsStepId.requestConfig = getApiV1ThreadsThreadIdRunsRunIdStepsStepIdRequestConfig;

/**
 * 接口 [Submit Tool Ouputs To Run↗](https://yapi.com/project/926/interface/api/70422) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequest {
    /**
     * A list of tools for which the outputs are being submitted.
     */
    tool_outputs: {
        /**
         * The ID of the tool call in the `required_action` object within the run object the output is being submitted for.
         */
        tool_call_id?: string;
        /**
         * The output of the tool call to be submitted to continue the run.
         */
        output?: string;
    }[];
    thread_id: string;
    run_id: string;
}

/**
 * 接口 [Submit Tool Ouputs To Run↗](https://yapi.com/project/926/interface/api/70422) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Submit Tool Ouputs To Run↗](https://yapi.com/project/926/interface/api/70422) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs',
        undefined,
        'thread_id' | 'run_id',
        string,
        false
    >
>;

/**
 * 接口 [Submit Tool Ouputs To Run↗](https://yapi.com/project/926/interface/api/70422) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequestConfig: PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_3_0_0_0,
        devUrl: devUrl_3_0_0_0,
        prodUrl: prodUrl_3_0_0_0,
        path: '/api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs',
        method: Method.POST,
        requestHeaders: {},
        requestBodyType: RequestBodyType.json,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_3_0_0_0,
        paramNames: ['thread_id', 'run_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputs',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Submit Tool Ouputs To Run↗](https://yapi.com/project/926/interface/api/70422) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputs = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsResponse>(
        prepare(postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputs.requestConfig =
    postApiV1ThreadsThreadIdRunsRunIdSubmitToolOutputsRequestConfig;

/**
 * 接口 [Create Thread And Run↗](https://yapi.com/project/926/interface/api/70428) 的 **请求类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsRunsRequest {
    assistant_id: string;
    thread?: {
        object?: string;
        messages?: {
            role: string;
            content: string;
            file_ids?: unknown[];
            metadata_?: {};
        }[];
    };
    instructions?: string;
    model?: string;
    metadata_?: {};
    tools?: unknown[];
}

/**
 * 接口 [Create Thread And Run↗](https://yapi.com/project/926/interface/api/70428) 的 **返回类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsRunsResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    instructions?: string;
    model?: string;
    status?: string;
    assistant_id: string;
    thread_id?: string;
    object?: string;
    file_ids?: unknown[];
    metadata_?: {};
    last_error?: {};
    required_action?: {};
    tools?: unknown[];
    started_at?: string;
    completed_at?: string;
    cancelled_at?: string;
    expires_at?: string;
    failed_at?: string;
}

/**
 * 接口 [Create Thread And Run↗](https://yapi.com/project/926/interface/api/70428) 的 **请求配置的类型**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsRunsRequestConfig = Readonly<
    RequestConfig<'https://yapi.com/mock/926', '', '', '/api/v1/threads/runs', undefined, string, string, false>
>;

/**
 * 接口 [Create Thread And Run↗](https://yapi.com/project/926/interface/api/70428) 的 **请求配置**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsRunsRequestConfig: PostApiV1ThreadsRunsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_3_0_0_0,
    devUrl: devUrl_3_0_0_0,
    prodUrl: prodUrl_3_0_0_0,
    path: '/api/v1/threads/runs',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_3_0_0_0,
    paramNames: [],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1ThreadsRuns',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create Thread And Run↗](https://yapi.com/project/926/interface/api/70428) 的 **请求函数**
 *
 * @分类 [runs↗](https://yapi.com/project/926/interface/api/cat_11480)
 * @标签 `runs`
 * @请求头 `POST /api/v1/threads/runs`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsRuns = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsRunsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsRunsResponse>(prepare(postApiV1ThreadsRunsRequestConfig, requestData), ...args);
};

postApiV1ThreadsRuns.requestConfig = postApiV1ThreadsRunsRequestConfig;

/* prettier-ignore-end */
