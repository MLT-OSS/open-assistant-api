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

const mockUrl_2_0_0_0 = 'https://yapi.com/mock/926' as any;
const devUrl_2_0_0_0 = '' as any;
const prodUrl_2_0_0_0 = '' as any;
const dataKey_2_0_0_0 = undefined as any;

/**
 * 接口 [List Messages↗](https://yapi.com/project/926/interface/api/70344) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
    thread_id: string;
}

/**
 * 接口 [List Messages↗](https://yapi.com/project/926/interface/api/70344) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesResponse {
    object?: string;
    data?: {
        id?: string;
        created_at?: string;
        updated_at?: string;
        role: string;
        thread_id: string;
        object?: string;
        content?: unknown[];
        file_ids?: unknown[];
        metadata_?: {};
        assistant_id?: string;
        run_id?: string;
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Messages↗](https://yapi.com/project/926/interface/api/70344) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdMessagesRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages',
        undefined,
        'thread_id',
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Messages↗](https://yapi.com/project/926/interface/api/70344) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdMessagesRequestConfig: GetApiV1ThreadsThreadIdMessagesRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_2_0_0_0,
    devUrl: devUrl_2_0_0_0,
    prodUrl: prodUrl_2_0_0_0,
    path: '/api/v1/threads/{thread_id}/messages',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_2_0_0_0,
    paramNames: ['thread_id'],
    queryNames: ['limit', 'order', 'after', 'before'],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1ThreadsThreadIdMessages',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [List Messages↗](https://yapi.com/project/926/interface/api/70344) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdMessages = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdMessagesRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdMessagesResponse>(
        prepare(getApiV1ThreadsThreadIdMessagesRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdMessages.requestConfig = getApiV1ThreadsThreadIdMessagesRequestConfig;

/**
 * 接口 [Create Message↗](https://yapi.com/project/926/interface/api/70350) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdMessagesRequest {
    role: string;
    content: string;
    file_ids?: unknown[];
    metadata_?: {};
    thread_id: string;
}

/**
 * 接口 [Create Message↗](https://yapi.com/project/926/interface/api/70350) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdMessagesResponse {
    id?: string;
    created_at?: string;
    updated_at?: string;
    role: string;
    thread_id: string;
    object?: string;
    content?: unknown[];
    file_ids?: unknown[];
    metadata_?: {};
    assistant_id?: string;
    run_id?: string;
}

/**
 * 接口 [Create Message↗](https://yapi.com/project/926/interface/api/70350) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdMessagesRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages',
        undefined,
        'thread_id',
        string,
        false
    >
>;

/**
 * 接口 [Create Message↗](https://yapi.com/project/926/interface/api/70350) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdMessagesRequestConfig: PostApiV1ThreadsThreadIdMessagesRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_2_0_0_0,
    devUrl: devUrl_2_0_0_0,
    prodUrl: prodUrl_2_0_0_0,
    path: '/api/v1/threads/{thread_id}/messages',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_2_0_0_0,
    paramNames: ['thread_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1ThreadsThreadIdMessages',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create Message↗](https://yapi.com/project/926/interface/api/70350) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdMessages = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdMessagesRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdMessagesResponse>(
        prepare(postApiV1ThreadsThreadIdMessagesRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdMessages.requestConfig = postApiV1ThreadsThreadIdMessagesRequestConfig;

/**
 * 接口 [Get Message↗](https://yapi.com/project/926/interface/api/70356) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdRequest {
    thread_id: string;
    message_id: string;
}

/**
 * 接口 [Get Message↗](https://yapi.com/project/926/interface/api/70356) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdResponse {
    id?: string;
    created_at?: string;
    updated_at?: string;
    role: string;
    thread_id: string;
    object?: string;
    content?: unknown[];
    file_ids?: unknown[];
    metadata_?: {};
    assistant_id?: string;
    run_id?: string;
}

/**
 * 接口 [Get Message↗](https://yapi.com/project/926/interface/api/70356) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdMessagesMessageIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages/{message_id}',
        undefined,
        'thread_id' | 'message_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Message↗](https://yapi.com/project/926/interface/api/70356) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdMessagesMessageIdRequestConfig: GetApiV1ThreadsThreadIdMessagesMessageIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_2_0_0_0,
        devUrl: devUrl_2_0_0_0,
        prodUrl: prodUrl_2_0_0_0,
        path: '/api/v1/threads/{thread_id}/messages/{message_id}',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_2_0_0_0,
        paramNames: ['thread_id', 'message_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1ThreadsThreadIdMessagesMessageId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Get Message↗](https://yapi.com/project/926/interface/api/70356) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdMessagesMessageId = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdMessagesMessageIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdMessagesMessageIdResponse>(
        prepare(getApiV1ThreadsThreadIdMessagesMessageIdRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdMessagesMessageId.requestConfig = getApiV1ThreadsThreadIdMessagesMessageIdRequestConfig;

/**
 * 接口 [Modify Message↗](https://yapi.com/project/926/interface/api/70362) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdMessagesMessageIdRequest {
    metadata_?: {};
    thread_id: string;
    message_id: string;
}

/**
 * 接口 [Modify Message↗](https://yapi.com/project/926/interface/api/70362) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1ThreadsThreadIdMessagesMessageIdResponse {
    id?: string;
    created_at?: string;
    updated_at?: string;
    role: string;
    thread_id: string;
    object?: string;
    content?: unknown[];
    file_ids?: unknown[];
    metadata_?: {};
    assistant_id?: string;
    run_id?: string;
}

/**
 * 接口 [Modify Message↗](https://yapi.com/project/926/interface/api/70362) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1ThreadsThreadIdMessagesMessageIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages/{message_id}',
        undefined,
        'thread_id' | 'message_id',
        string,
        false
    >
>;

/**
 * 接口 [Modify Message↗](https://yapi.com/project/926/interface/api/70362) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1ThreadsThreadIdMessagesMessageIdRequestConfig: PostApiV1ThreadsThreadIdMessagesMessageIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_2_0_0_0,
        devUrl: devUrl_2_0_0_0,
        prodUrl: prodUrl_2_0_0_0,
        path: '/api/v1/threads/{thread_id}/messages/{message_id}',
        method: Method.POST,
        requestHeaders: {},
        requestBodyType: RequestBodyType.json,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_2_0_0_0,
        paramNames: ['thread_id', 'message_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'postApiV1ThreadsThreadIdMessagesMessageId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Modify Message↗](https://yapi.com/project/926/interface/api/70362) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `POST /api/v1/threads/{thread_id}/messages/{message_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1ThreadsThreadIdMessagesMessageId = /*#__PURE__*/ (
    requestData: PostApiV1ThreadsThreadIdMessagesMessageIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1ThreadsThreadIdMessagesMessageIdResponse>(
        prepare(postApiV1ThreadsThreadIdMessagesMessageIdRequestConfig, requestData),
        ...args
    );
};

postApiV1ThreadsThreadIdMessagesMessageId.requestConfig = postApiV1ThreadsThreadIdMessagesMessageIdRequestConfig;

/**
 * 接口 [List Message Files↗](https://yapi.com/project/926/interface/api/70368) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdFilesRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
    message_id: string;
    thread_id: string;
}

/**
 * 接口 [List Message Files↗](https://yapi.com/project/926/interface/api/70368) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdFilesResponse {
    object?: string;
    data?: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        message_id: string;
        object?: string;
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Message Files↗](https://yapi.com/project/926/interface/api/70368) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdMessagesMessageIdFilesRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages/{message_id}/files',
        undefined,
        'message_id' | 'thread_id',
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Message Files↗](https://yapi.com/project/926/interface/api/70368) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdMessagesMessageIdFilesRequestConfig: GetApiV1ThreadsThreadIdMessagesMessageIdFilesRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_2_0_0_0,
        devUrl: devUrl_2_0_0_0,
        prodUrl: prodUrl_2_0_0_0,
        path: '/api/v1/threads/{thread_id}/messages/{message_id}/files',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_2_0_0_0,
        paramNames: ['message_id', 'thread_id'],
        queryNames: ['limit', 'order', 'after', 'before'],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1ThreadsThreadIdMessagesMessageIdFiles',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [List Message Files↗](https://yapi.com/project/926/interface/api/70368) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdMessagesMessageIdFiles = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdMessagesMessageIdFilesRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdMessagesMessageIdFilesResponse>(
        prepare(getApiV1ThreadsThreadIdMessagesMessageIdFilesRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdMessagesMessageIdFiles.requestConfig =
    getApiV1ThreadsThreadIdMessagesMessageIdFilesRequestConfig;

/**
 * 接口 [Get Message File↗](https://yapi.com/project/926/interface/api/70374) 的 **请求类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequest {
    thread_id: string;
    message_id: string;
    file_id: string;
}

/**
 * 接口 [Get Message File↗](https://yapi.com/project/926/interface/api/70374) 的 **返回类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdResponse {
    /**
     * The identifier, which can be referenced in API endpoints.
     */
    id: string;
    object?: string;
    /**
     * The Unix timestamp (in seconds) for when the message file was created.
     */
    created_at: number;
    /**
     * The ID of the [message](/docs/api-reference/messages) that the [File](/docs/api-reference/files) is attached to.
     */
    message_id: string;
}

/**
 * 接口 [Get Message File↗](https://yapi.com/project/926/interface/api/70374) 的 **请求配置的类型**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}',
        undefined,
        'thread_id' | 'message_id' | 'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Message File↗](https://yapi.com/project/926/interface/api/70374) 的 **请求配置**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequestConfig: GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_2_0_0_0,
        devUrl: devUrl_2_0_0_0,
        prodUrl: prodUrl_2_0_0_0,
        path: '/api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_2_0_0_0,
        paramNames: ['thread_id', 'message_id', 'file_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1ThreadsThreadIdMessagesMessageIdFilesFileId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Get Message File↗](https://yapi.com/project/926/interface/api/70374) 的 **请求函数**
 *
 * @分类 [messages↗](https://yapi.com/project/926/interface/api/cat_11478)
 * @标签 `messages`
 * @请求头 `GET /api/v1/threads/{thread_id}/messages/{message_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1ThreadsThreadIdMessagesMessageIdFilesFileId = /*#__PURE__*/ (
    requestData: GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdResponse>(
        prepare(getApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequestConfig, requestData),
        ...args
    );
};

getApiV1ThreadsThreadIdMessagesMessageIdFilesFileId.requestConfig =
    getApiV1ThreadsThreadIdMessagesMessageIdFilesFileIdRequestConfig;

/* prettier-ignore-end */
