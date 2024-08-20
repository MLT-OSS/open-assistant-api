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

const mockUrl_1_0_0_0 = 'https://yapi.com/mock/926' as any;
const devUrl_1_0_0_0 = '' as any;
const prodUrl_1_0_0_0 = '' as any;
const dataKey_1_0_0_0 = undefined as any;

/**
 * 接口 [Create Thread↗](https://yapi.com/project/926/interface/api/70320) 的 **请求类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsRequest {
    object?: string;
    messages?: {
        role: string;
        content: string;
        file_ids?: unknown[];
        metadata_?: {};
    }[];
}

/**
 * 接口 [Create Thread↗](https://yapi.com/project/926/interface/api/70320) 的 **返回类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    object?: string;
    metadata_?: {};
}

/**
 * 接口 [Create Thread↗](https://yapi.com/project/926/interface/api/70320) 的 **请求配置的类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsRequestConfig = Readonly<
    RequestConfig<'https://yapi.com/mock/926', '', '', '/api/v1/threads', undefined, string, string, false>
>;

/**
 * 接口 [Create Thread↗](https://yapi.com/project/926/interface/api/70320) 的 **请求配置**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsRequestConfig: PostApiV1ThreadsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_1_0_0_0,
    devUrl: devUrl_1_0_0_0,
    prodUrl: prodUrl_1_0_0_0,
    path: '/api/v1/threads',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_1_0_0_0,
    paramNames: [],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1Threads',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create Thread↗](https://yapi.com/project/926/interface/api/70320) 的 **请求函数**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1Threads = /*#__PURE__*/ (requestData: PostApiV1ThreadsRequest, ...args: UserRequestRestArgs) => {
    return request<PostApiV1ThreadsResponse>(prepare(postApiV1ThreadsRequestConfig, requestData), ...args);
};

postApiV1Threads.requestConfig = postApiV1ThreadsRequestConfig;

/**
 * 接口 [Get Thread↗](https://yapi.com/project/926/interface/api/70326) 的 **请求类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `GET /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdRequest {
    thread_id: string;
}

/**
 * 接口 [Get Thread↗](https://yapi.com/project/926/interface/api/70326) 的 **返回类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `GET /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    object?: string;
    metadata_?: {};
}

/**
 * 接口 [Get Thread↗](https://yapi.com/project/926/interface/api/70326) 的 **请求配置的类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `GET /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}',
        undefined,
        'thread_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Thread↗](https://yapi.com/project/926/interface/api/70326) 的 **请求配置**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `GET /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdRequestConfig: GetApiV1ThreadsThreadIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_1_0_0_0,
    devUrl: devUrl_1_0_0_0,
    prodUrl: prodUrl_1_0_0_0,
    path: '/api/v1/threads/{thread_id}',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_1_0_0_0,
    paramNames: ['thread_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1ThreadsThreadId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Get Thread↗](https://yapi.com/project/926/interface/api/70326) 的 **请求函数**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `GET /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadId = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdResponse>(
        prepare(getApiV1ThreadsThreadIdRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadId.requestConfig = getApiV1ThreadsThreadIdRequestConfig;

/**
 * 接口 [Modify Thread↗](https://yapi.com/project/926/interface/api/70332) 的 **请求类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdRequest {
    metadata?: {};
    thread_id: string;
}

/**
 * 接口 [Modify Thread↗](https://yapi.com/project/926/interface/api/70332) 的 **返回类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    object?: string;
    metadata_?: {};
}

/**
 * 接口 [Modify Thread↗](https://yapi.com/project/926/interface/api/70332) 的 **请求配置的类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}',
        undefined,
        'thread_id',
        string,
        false
    >
>;

/**
 * 接口 [Modify Thread↗](https://yapi.com/project/926/interface/api/70332) 的 **请求配置**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdRequestConfig: PostApiV1ThreadsThreadIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_1_0_0_0,
    devUrl: devUrl_1_0_0_0,
    prodUrl: prodUrl_1_0_0_0,
    path: '/api/v1/threads/{thread_id}',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_1_0_0_0,
    paramNames: ['thread_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1ThreadsThreadId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Modify Thread↗](https://yapi.com/project/926/interface/api/70332) 的 **请求函数**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `POST /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadId = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdResponse>(
        prepare(postApiV1ThreadsThreadIdRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadId.requestConfig = postApiV1ThreadsThreadIdRequestConfig;

/**
 * 接口 [Delete Thread↗](https://yapi.com/project/926/interface/api/70338) 的 **请求类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `DELETE /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface DeleteApiV1ThreadsThreadIdRequest {
    thread_id: string;
}

/**
 * 接口 [Delete Thread↗](https://yapi.com/project/926/interface/api/70338) 的 **返回类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `DELETE /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface DeleteApiV1ThreadsThreadIdResponse {
    id: string;
    object?: string;
    deleted: boolean;
}

/**
 * 接口 [Delete Thread↗](https://yapi.com/project/926/interface/api/70338) 的 **请求配置的类型**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `DELETE /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type DeleteApiV1ThreadsThreadIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}',
        undefined,
        'thread_id',
        string,
        false
    >
>;

/**
 * 接口 [Delete Thread↗](https://yapi.com/project/926/interface/api/70338) 的 **请求配置**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `DELETE /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const deleteApiV1ThreadsThreadIdRequestConfig: DeleteApiV1ThreadsThreadIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_1_0_0_0,
    devUrl: devUrl_1_0_0_0,
    prodUrl: prodUrl_1_0_0_0,
    path: '/api/v1/threads/{thread_id}',
    method: Method.DELETE,
    requestHeaders: {},
    requestBodyType: RequestBodyType.raw,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_1_0_0_0,
    paramNames: ['thread_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'deleteApiV1ThreadsThreadId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Delete Thread↗](https://yapi.com/project/926/interface/api/70338) 的 **请求函数**
 *
 * @分类 [threads↗](https://yapi.com/project/926/interface/api/cat_11476)
 * @标签 `threads`
 * @请求头 `DELETE /api/v1/threads/{thread_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const deleteApiV1ThreadsThreadId = /*#__PURE__*/ (
    requestData: DeleteApiV1ThreadsThreadIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<DeleteApiV1ThreadsThreadIdResponse>(
        prepare(deleteApiV1ThreadsThreadIdRequestConfig, requestData),
        ...args
    );
};

deleteApiV1ThreadsThreadId.requestConfig = deleteApiV1ThreadsThreadIdRequestConfig;

/* prettier-ignore-end */
