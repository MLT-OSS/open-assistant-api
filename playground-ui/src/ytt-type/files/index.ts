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

const mockUrl_4_0_0_0 = 'https://yapi.com/mock/926' as any;
const devUrl_4_0_0_0 = '' as any;
const prodUrl_4_0_0_0 = '' as any;
const dataKey_4_0_0_0 = undefined as any;

/**
 * 接口 [List Files↗](https://yapi.com/project/926/interface/api/70434) 的 **请求类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1FilesRequest {
    purpose?: string;
}

/**
 * 接口 [List Files↗](https://yapi.com/project/926/interface/api/70434) 的 **返回类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1FilesResponse {
    data: {
        created_at?: string;
        updated_at?: string;
        id?: string;
        bytes: number;
        filename: string;
        purpose: string;
        object?: string;
        key: string;
        status?: string;
        status_details?: string;
    }[];
    object?: string;
}

/**
 * 接口 [List Files↗](https://yapi.com/project/926/interface/api/70434) 的 **请求配置的类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1FilesRequestConfig = Readonly<
    RequestConfig<'https://yapi.com/mock/926', '', '', '/api/v1/files', undefined, string, 'purpose', false>
>;

/**
 * 接口 [List Files↗](https://yapi.com/project/926/interface/api/70434) 的 **请求配置**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1FilesRequestConfig: GetApiV1FilesRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_4_0_0_0,
    devUrl: devUrl_4_0_0_0,
    prodUrl: prodUrl_4_0_0_0,
    path: '/api/v1/files',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_4_0_0_0,
    paramNames: [],
    queryNames: ['purpose'],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1Files',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [List Files↗](https://yapi.com/project/926/interface/api/70434) 的 **请求函数**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1Files = /*#__PURE__*/ (requestData: GetApiV1FilesRequest, ...args: UserRequestRestArgs) => {
    return request<GetApiV1FilesResponse>(prepare(getApiV1FilesRequestConfig, requestData), ...args);
};

getApiV1Files.requestConfig = getApiV1FilesRequestConfig;

/**
 * 接口 [Create File↗](https://yapi.com/project/926/interface/api/70440) 的 **请求类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `POST /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1FilesRequest {}

/**
 * 接口 [Create File↗](https://yapi.com/project/926/interface/api/70440) 的 **返回类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `POST /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface PostApiV1FilesResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    bytes: number;
    filename: string;
    purpose: string;
    object?: string;
    key: string;
    status?: string;
    status_details?: string;
}

/**
 * 接口 [Create File↗](https://yapi.com/project/926/interface/api/70440) 的 **请求配置的类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `POST /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
type PostApiV1FilesRequestConfig = Readonly<
    RequestConfig<'https://yapi.com/mock/926', '', '', '/api/v1/files', undefined, string, string, true>
>;

/**
 * 接口 [Create File↗](https://yapi.com/project/926/interface/api/70440) 的 **请求配置**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `POST /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
const postApiV1FilesRequestConfig: PostApiV1FilesRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_4_0_0_0,
    devUrl: devUrl_4_0_0_0,
    prodUrl: prodUrl_4_0_0_0,
    path: '/api/v1/files',
    method: Method.POST,
    requestHeaders: {},
    requestBodyType: RequestBodyType.json,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_4_0_0_0,
    paramNames: [],
    queryNames: [],
    requestDataOptional: true,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'postApiV1Files',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Create File↗](https://yapi.com/project/926/interface/api/70440) 的 **请求函数**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `POST /api/v1/files`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const postApiV1Files = /*#__PURE__*/ (requestData?: PostApiV1FilesRequest, ...args: UserRequestRestArgs) => {
    return request<PostApiV1FilesResponse>(prepare(postApiV1FilesRequestConfig, requestData), ...args);
};

postApiV1Files.requestConfig = postApiV1FilesRequestConfig;

/**
 * 接口 [Retrieve File↗](https://yapi.com/project/926/interface/api/70446) 的 **请求类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1FilesFileIdRequest {
    file_id: string;
}

/**
 * 接口 [Retrieve File↗](https://yapi.com/project/926/interface/api/70446) 的 **返回类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1FilesFileIdResponse {
    created_at?: string;
    updated_at?: string;
    id?: string;
    bytes: number;
    filename: string;
    purpose: string;
    object?: string;
    key: string;
    status?: string;
    status_details?: string;
}

/**
 * 接口 [Retrieve File↗](https://yapi.com/project/926/interface/api/70446) 的 **请求配置的类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1FilesFileIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/files/{file_id}',
        undefined,
        'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Retrieve File↗](https://yapi.com/project/926/interface/api/70446) 的 **请求配置**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1FilesFileIdRequestConfig: GetApiV1FilesFileIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_4_0_0_0,
    devUrl: devUrl_4_0_0_0,
    prodUrl: prodUrl_4_0_0_0,
    path: '/api/v1/files/{file_id}',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_4_0_0_0,
    paramNames: ['file_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1FilesFileId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Retrieve File↗](https://yapi.com/project/926/interface/api/70446) 的 **请求函数**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1FilesFileId = /*#__PURE__*/ (
    requestData: GetApiV1FilesFileIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1FilesFileIdResponse>(prepare(getApiV1FilesFileIdRequestConfig, requestData), ...args);
};

getApiV1FilesFileId.requestConfig = getApiV1FilesFileIdRequestConfig;

/**
 * 接口 [Delete File↗](https://yapi.com/project/926/interface/api/70452) 的 **请求类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `DELETE /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface DeleteApiV1FilesFileIdRequest {
    file_id: string;
}

/**
 * 接口 [Delete File↗](https://yapi.com/project/926/interface/api/70452) 的 **返回类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `DELETE /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface DeleteApiV1FilesFileIdResponse {
    id: string;
    object?: string;
    deleted: boolean;
}

/**
 * 接口 [Delete File↗](https://yapi.com/project/926/interface/api/70452) 的 **请求配置的类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `DELETE /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
type DeleteApiV1FilesFileIdRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/files/{file_id}',
        undefined,
        'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Delete File↗](https://yapi.com/project/926/interface/api/70452) 的 **请求配置**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `DELETE /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
const deleteApiV1FilesFileIdRequestConfig: DeleteApiV1FilesFileIdRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_4_0_0_0,
    devUrl: devUrl_4_0_0_0,
    prodUrl: prodUrl_4_0_0_0,
    path: '/api/v1/files/{file_id}',
    method: Method.DELETE,
    requestHeaders: {},
    requestBodyType: RequestBodyType.raw,
    responseBodyType: ResponseBodyType.json,
    dataKey: dataKey_4_0_0_0,
    paramNames: ['file_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'deleteApiV1FilesFileId',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Delete File↗](https://yapi.com/project/926/interface/api/70452) 的 **请求函数**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `DELETE /api/v1/files/{file_id}`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const deleteApiV1FilesFileId = /*#__PURE__*/ (
    requestData: DeleteApiV1FilesFileIdRequest,
    ...args: UserRequestRestArgs
) => {
    return request<DeleteApiV1FilesFileIdResponse>(prepare(deleteApiV1FilesFileIdRequestConfig, requestData), ...args);
};

deleteApiV1FilesFileId.requestConfig = deleteApiV1FilesFileIdRequestConfig;

/**
 * 接口 [Download File↗](https://yapi.com/project/926/interface/api/70458) 的 **请求类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}/content`
 * @更新时间 `2023-12-26 15:01:28`
 */
export interface GetApiV1FilesFileIdContentRequest {
    file_id: string;
}

/**
 * 接口 [Download File↗](https://yapi.com/project/926/interface/api/70458) 的 **返回类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}/content`
 * @更新时间 `2023-12-26 15:01:28`
 */
export type GetApiV1FilesFileIdContentResponse = any;

/**
 * 接口 [Download File↗](https://yapi.com/project/926/interface/api/70458) 的 **请求配置的类型**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}/content`
 * @更新时间 `2023-12-26 15:01:28`
 */
type GetApiV1FilesFileIdContentRequestConfig = Readonly<
    RequestConfig<
        'https://yapi.com/mock/926',
        '',
        '',
        '/api/v1/files/{file_id}/content',
        undefined,
        'file_id',
        string,
        false
    >
>;

/**
 * 接口 [Download File↗](https://yapi.com/project/926/interface/api/70458) 的 **请求配置**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}/content`
 * @更新时间 `2023-12-26 15:01:28`
 */
const getApiV1FilesFileIdContentRequestConfig: GetApiV1FilesFileIdContentRequestConfig = /*#__PURE__*/ {
    mockUrl: mockUrl_4_0_0_0,
    devUrl: devUrl_4_0_0_0,
    prodUrl: prodUrl_4_0_0_0,
    path: '/api/v1/files/{file_id}/content',
    method: Method.GET,
    requestHeaders: {},
    requestBodyType: RequestBodyType.query,
    responseBodyType: ResponseBodyType.raw,
    dataKey: dataKey_4_0_0_0,
    paramNames: ['file_id'],
    queryNames: [],
    requestDataOptional: false,
    requestDataJsonSchema: {},
    responseDataJsonSchema: {},
    requestFunctionName: 'getApiV1FilesFileIdContent',
    queryStringArrayFormat: QueryStringArrayFormat.brackets,
    extraInfo: {}
};

/**
 * 接口 [Download File↗](https://yapi.com/project/926/interface/api/70458) 的 **请求函数**
 *
 * @分类 [files↗](https://yapi.com/project/926/interface/api/cat_11482)
 * @标签 `files`
 * @请求头 `GET /api/v1/files/{file_id}/content`
 * @更新时间 `2023-12-26 15:01:28`
 */
export const getApiV1FilesFileIdContent = /*#__PURE__*/ (
    requestData: GetApiV1FilesFileIdContentRequest,
    ...args: UserRequestRestArgs
) => {
    return request<GetApiV1FilesFileIdContentResponse>(
        prepare(getApiV1FilesFileIdContentRequestConfig, requestData),
        ...args
    );
};

getApiV1FilesFileIdContent.requestConfig = getApiV1FilesFileIdContentRequestConfig;

/* prettier-ignore-end */
