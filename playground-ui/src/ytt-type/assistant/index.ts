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

const mockUrl_0_0_0_0 = 'https://yapi.com/mock/926' as any;
const devUrl_0_0_0_0 = '' as any;
const prodUrl_0_0_0_0 = '' as any;
const dataKey_0_0_0_0 = undefined as any;

/**
 * 接口 [List Assistants↗](https://yapi.com/project/926/interface/api/70266) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
}

/**
 * 接口 [List Assistants↗](https://yapi.com/project/926/interface/api/70266) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsResponse {
    object?: string;
    data?: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        model: string;
        object?: string;
        description?: string;
        file_ids?: unknown[];
        instructions?: string;
        metadata_?: {};
        name?: string;
        tools?: unknown[];
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Assistants↗](https://yapi.com/project/926/interface/api/70266) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
type GetApiV1AssistantsRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants',
        undefined,
        string,
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Assistants↗](https://yapi.com/project/926/interface/api/70266) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
const getApiV1AssistantsRequestConfig: GetApiV1AssistantsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: [],
    queryNames: ['limit', 'order', 'after', 'before'],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1Assistants',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [List Assistants↗](https://yapi.com/project/926/interface/api/70266) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const getApiV1Assistants = /*#__PURE__*/ (
    requestData: GetApiV1AssistantsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1AssistantsResponse>(prepare(getApiV1AssistantsRequestConfig, requestData), ...args);
};

getApiV1Assistants.requestConfig = getApiV1AssistantsRequestConfig;

/**
 * 接口 [Create Assistant↗](https://yapi.com/project/926/interface/api/70272) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsRequest {
    created_at?: string;
    updated_at?: string;
    id?: string;
    model: string;
    object?: string;
    description?: string;
    file_ids?: unknown[];
    instructions?: string;
    metadata_?: {};
    name?: string;
    tools?: unknown[];
}

/**
 * 接口 [Create Assistant↗](https://yapi.com/project/926/interface/api/70272) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    model: string;
    object?: string;
    description?: string;
    file_ids?: unknown[];
    instructions?: string;
    metadata_?: {};
    name?: string;
    tools?: unknown[];
}

/**
 * 接口 [Create Assistant↗](https://yapi.com/project/926/interface/api/70272) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
type PostApiV1AssistantsRequestConfig = Readonly<
    RequestConfig<'https://yapi.com/mock/926', '', '', '/api/v1/assistants', undefined, string, string, false>
>;

/**
 * 接口 [Create Assistant↗](https://yapi.com/project/926/interface/api/70272) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
const postApiV1AssistantsRequestConfig: PostApiV1AssistantsRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: [],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1Assistants',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create Assistant↗](https://yapi.com/project/926/interface/api/70272) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const postApiV1Assistants = /*#__PURE__*/ (
    requestData: PostApiV1AssistantsRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1AssistantsResponse>(prepare(postApiV1AssistantsRequestConfig, requestData), ...args);
};

postApiV1Assistants.requestConfig = postApiV1AssistantsRequestConfig;

/**
 * 接口 [Get Assistant↗](https://yapi.com/project/926/interface/api/70278) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdRequest {
    assistant_id: string;
}

/**
 * 接口 [Get Assistant↗](https://yapi.com/project/926/interface/api/70278) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    model: string;
    object?: string;
    description?: string;
    file_ids?: unknown[];
    instructions?: string;
    metadata_?: {};
    name?: string;
    tools?: unknown[];
}

/**
 * 接口 [Get Assistant↗](https://yapi.com/project/926/interface/api/70278) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
type GetApiV1AssistantsAssistantIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}',
        undefined,
        'assistant_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Assistant↗](https://yapi.com/project/926/interface/api/70278) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
const getApiV1AssistantsAssistantIdRequestConfig: GetApiV1AssistantsAssistantIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants/{assistant_id}',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: ['assistant_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1AssistantsAssistantId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Get Assistant↗](https://yapi.com/project/926/interface/api/70278) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const getApiV1AssistantsAssistantId = /*#__PURE__*/ (
    requestData: GetApiV1AssistantsAssistantIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1AssistantsAssistantIdResponse>(
        prepare(getApiV1AssistantsAssistantIdRequestConfig, requestData),
        ...args
    );
};

getApiV1AssistantsAssistantId.requestConfig = getApiV1AssistantsAssistantIdRequestConfig;

/**
 * 接口 [Modify Assistant↗](https://yapi.com/project/926/interface/api/70284) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsAssistantIdRequest {
    created_at?: string;
    updated_at?: string;
    id?: string;
    model: string;
    name?: string;
    description?: string;
    instructions?: string;
    tools?: unknown[];
    file_ids?: unknown[];
    metadata_?: {};
    assistant_id: string;
}

/**
 * 接口 [Modify Assistant↗](https://yapi.com/project/926/interface/api/70284) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsAssistantIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    model: string;
    object?: string;
    description?: string;
    file_ids?: unknown[];
    instructions?: string;
    metadata_?: {};
    name?: string;
    tools?: unknown[];
}

/**
 * 接口 [Modify Assistant↗](https://yapi.com/project/926/interface/api/70284) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
type PostApiV1AssistantsAssistantIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}',
        undefined,
        'assistant_id',
        string,
        false
    >
>;

/**
 * 接口 [Modify Assistant↗](https://yapi.com/project/926/interface/api/70284) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
const postApiV1AssistantsAssistantIdRequestConfig: PostApiV1AssistantsAssistantIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants/{assistant_id}',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: ['assistant_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1AssistantsAssistantId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Modify Assistant↗](https://yapi.com/project/926/interface/api/70284) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const postApiV1AssistantsAssistantId = /*#__PURE__*/ (
    requestData: PostApiV1AssistantsAssistantIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1AssistantsAssistantIdResponse>(
        prepare(postApiV1AssistantsAssistantIdRequestConfig, requestData),
        ...args
    );
};

postApiV1AssistantsAssistantId.requestConfig = postApiV1AssistantsAssistantIdRequestConfig;

/**
 * 接口 [Delete Assistant↗](https://yapi.com/project/926/interface/api/70290) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface DeleteApiV1AssistantsAssistantIdRequest {
    assistant_id: string;
}

/**
 * 接口 [Delete Assistant↗](https://yapi.com/project/926/interface/api/70290) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface DeleteApiV1AssistantsAssistantIdResponse {
    id: string;
    object?: string;
    deleted: boolean;
}

/**
 * 接口 [Delete Assistant↗](https://yapi.com/project/926/interface/api/70290) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
type DeleteApiV1AssistantsAssistantIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}',
        undefined,
        'assistant_id',
        string,
        false
    >
>;

/**
 * 接口 [Delete Assistant↗](https://yapi.com/project/926/interface/api/70290) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
const deleteApiV1AssistantsAssistantIdRequestConfig: DeleteApiV1AssistantsAssistantIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants/{assistant_id}',
    method: Method.DELETE,
    requestHeaders: {},
    requestBodyType: RequestBodyType.raw,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: ['assistant_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'deleteApiV1AssistantsAssistantId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Delete Assistant↗](https://yapi.com/project/926/interface/api/70290) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const deleteApiV1AssistantsAssistantId = /*#__PURE__*/ (
    requestData: DeleteApiV1AssistantsAssistantIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<DeleteApiV1AssistantsAssistantIdResponse>(
        prepare(deleteApiV1AssistantsAssistantIdRequestConfig, requestData),
        ...args
    );
};

deleteApiV1AssistantsAssistantId.requestConfig = deleteApiV1AssistantsAssistantIdRequestConfig;

/**
 * 接口 [List Assistant Files↗](https://yapi.com/project/926/interface/api/70296) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdFilesRequest {
    limit?: string;
    order?: string;
    after?: string;
    before?: string;
    assistant_id: string;
}

/**
 * 接口 [List Assistant Files↗](https://yapi.com/project/926/interface/api/70296) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdFilesResponse {
    object?: string;
    data?: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        assistant_id: string;
        object?: string;
    }[];
    first_id?: string;
    last_id?: string;
    has_more?: boolean;
}

/**
 * 接口 [List Assistant Files↗](https://yapi.com/project/926/interface/api/70296) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
type GetApiV1AssistantsAssistantIdFilesRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}/files',
        undefined,
        'assistant_id',
        'limit' | 'order' | 'after' | 'before',
        false
    >
>;

/**
 * 接口 [List Assistant Files↗](https://yapi.com/project/926/interface/api/70296) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
const getApiV1AssistantsAssistantIdFilesRequestConfig: GetApiV1AssistantsAssistantIdFilesRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_0_0_0_0,
    devUrl: devUrl_0_0_0_0,
    prodUrl: prodUrl_0_0_0_0,
    path: '/api/v1/assistants/{assistant_id}/files',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_0_0_0_0,
    paramNames: ['assistant_id'],
    queryNames: ['limit', 'order', 'after', 'before'],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1AssistantsAssistantIdFiles',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [List Assistant Files↗](https://yapi.com/project/926/interface/api/70296) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const getApiV1AssistantsAssistantIdFiles = /*#__PURE__*/ (
    requestData: GetApiV1AssistantsAssistantIdFilesRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1AssistantsAssistantIdFilesResponse>(
        prepare(getApiV1AssistantsAssistantIdFilesRequestConfig, requestData),
        ...args
    );
};

getApiV1AssistantsAssistantIdFiles.requestConfig = getApiV1AssistantsAssistantIdFilesRequestConfig;

/**
 * 接口 [Create Assistant File↗](https://yapi.com/project/926/interface/api/70302) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsAssistantIdFilesRequest {
    assistant_id: string;
    object?: string;
}

/**
 * 接口 [Create Assistant File↗](https://yapi.com/project/926/interface/api/70302) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface PostApiV1AssistantsAssistantIdFilesResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    assistant_id: string;
    object?: string;
}

/**
 * 接口 [Create Assistant File↗](https://yapi.com/project/926/interface/api/70302) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
type PostApiV1AssistantsAssistantIdFilesRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}/files',
        undefined,
        'assistant_id',
        string,
        false
    >
>;

/**
 * 接口 [Create Assistant File↗](https://yapi.com/project/926/interface/api/70302) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
const postApiV1AssistantsAssistantIdFilesRequestConfig: PostApiV1AssistantsAssistantIdFilesRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_0_0_0_0,
        devUrl: devUrl_0_0_0_0,
        prodUrl: prodUrl_0_0_0_0,
        path: '/api/v1/assistants/{assistant_id}/files',
        method: Method.POST,
        requestHeaders: {},
        requestBodyType: RequestBodyType.json,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_0_0_0_0,
        paramNames: ['assistant_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'postApiV1AssistantsAssistantIdFiles',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Create Assistant File↗](https://yapi.com/project/926/interface/api/70302) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `POST /api/v1/assistants/{assistant_id}/files`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const postApiV1AssistantsAssistantIdFiles = /*#__PURE__*/ (
    requestData: PostApiV1AssistantsAssistantIdFilesRequest,
    ...args: UserRequestRestArgs
) => {
    return request<PostApiV1AssistantsAssistantIdFilesResponse>(
        prepare(postApiV1AssistantsAssistantIdFilesRequestConfig, requestData),
        ...args
    );
};

postApiV1AssistantsAssistantIdFiles.requestConfig = postApiV1AssistantsAssistantIdFilesRequestConfig;

/**
 * 接口 [Get Assistant File↗](https://yapi.com/project/926/interface/api/70308) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdFilesFileIdRequest {
    assistant_id: string;
    file_id: string;
}

/**
 * 接口 [Get Assistant File↗](https://yapi.com/project/926/interface/api/70308) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface GetApiV1AssistantsAssistantIdFilesFileIdResponse {
    /**
     * The identifier, which can be referenced in API endpoints.
     */
    id: string;
    /**
     * The object type, which is always `assistant.file`.
     */
    object: string;
    /**
     * The Unix timestamp (in seconds) for when the assistant file was created.
     */
    created_at: number;
    /**
     * The assistant ID that the file is attached to.
     */
    assistant_id: string;
}

/**
 * 接口 [Get Assistant File↗](https://yapi.com/project/926/interface/api/70308) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
type GetApiV1AssistantsAssistantIdFilesFileIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}/files/{file_id}',
        undefined,
        'assistant_id' | 'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Get Assistant File↗](https://yapi.com/project/926/interface/api/70308) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
const getApiV1AssistantsAssistantIdFilesFileIdRequestConfig: GetApiV1AssistantsAssistantIdFilesFileIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_0_0_0_0,
        devUrl: devUrl_0_0_0_0,
        prodUrl: prodUrl_0_0_0_0,
        path: '/api/v1/assistants/{assistant_id}/files/{file_id}',
        method: Method.GET,
        requestHeaders: {},
        requestBodyType: RequestBodyType.query,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_0_0_0_0,
        paramNames: ['assistant_id', 'file_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'getApiV1AssistantsAssistantIdFilesFileId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Get Assistant File↗](https://yapi.com/project/926/interface/api/70308) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `GET /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const getApiV1AssistantsAssistantIdFilesFileId = /*#__PURE__*/ (
    requestData: GetApiV1AssistantsAssistantIdFilesFileIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1AssistantsAssistantIdFilesFileIdResponse>(
        prepare(getApiV1AssistantsAssistantIdFilesFileIdRequestConfig, requestData),
        ...args
    );
};

getApiV1AssistantsAssistantIdFilesFileId.requestConfig = getApiV1AssistantsAssistantIdFilesFileIdRequestConfig;

/**
 * 接口 [Delete Assistant File↗](https://yapi.com/project/926/interface/api/70314) 的 **请求类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface DeleteApiV1AssistantsAssistantIdFilesFileIdRequest {
    assistant_id: string;
    file_id: string;
}

/**
 * 接口 [Delete Assistant File↗](https://yapi.com/project/926/interface/api/70314) 的 **返回类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export interface DeleteApiV1AssistantsAssistantIdFilesFileIdResponse {
    id: string;
    object?: string;
    deleted: boolean;
}

/**
 * 接口 [Delete Assistant File↗](https://yapi.com/project/926/interface/api/70314) 的 **请求配置的类型**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
type DeleteApiV1AssistantsAssistantIdFilesFileIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/assistants/{assistant_id}/files/{file_id}',
        undefined,
        'assistant_id' | 'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Delete Assistant File↗](https://yapi.com/project/926/interface/api/70314) 的 **请求配置**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
const deleteApiV1AssistantsAssistantIdFilesFileIdRequestConfig: DeleteApiV1AssistantsAssistantIdFilesFileIdRequestConfig =
    /*#__PURE__*/ {
        mockUrl: mockUrl_0_0_0_0,
        devUrl: devUrl_0_0_0_0,
        prodUrl: prodUrl_0_0_0_0,
        path: '/api/v1/assistants/{assistant_id}/files/{file_id}',
        method: Method.DELETE,
        requestHeaders: {},
        requestBodyType: RequestBodyType.raw,
        responseBodyType: ResponseBodyType.json,
        dataKey: dataKey_0_0_0_0,
        paramNames: ['assistant_id', 'file_id'],
        queryNames: [],
        requestDataOptional: false,
        requestDataJsonSchema: {},
        responseDataJsonSchema: {},
        requestFunctionName: 'deleteApiV1AssistantsAssistantIdFilesFileId',
        queryStringArrayFormat: QueryStringArrayFormat.brackets,
        extraInfo: {}
    };

/**
 * 接口 [Delete Assistant File↗](https://yapi.com/project/926/interface/api/70314) 的 **请求函数**
 *
 * @分类 [assistants↗](https://yapi.com/project/926/interface/api/cat_11474)
 * @标签 `assistants`
 * @请求头 `DELETE /api/v1/assistants/{assistant_id}/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:27`
 */
export const deleteApiV1AssistantsAssistantIdFilesFileId = /*#__PURE__*/ (
    requestData: DeleteApiV1AssistantsAssistantIdFilesFileIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<DeleteApiV1AssistantsAssistantIdFilesFileIdResponse>(
        prepare(deleteApiV1AssistantsAssistantIdFilesFileIdRequestConfig, requestData),
        ...args
    );
};

deleteApiV1AssistantsAssistantIdFilesFileId.requestConfig = deleteApiV1AssistantsAssistantIdFilesFileIdRequestConfig;

/* prettier-ignore-end */
