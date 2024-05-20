import HeaderLogo from '@/components/header-logo';
import HeaderRight from '@/components/header-right';
import adaptor, { errorThrower } from '@/utils/adaptor';
import errorHandler from '@/utils/error-handler';
import type { AxiosResponse, RequestConfig } from '@@/plugin-request/request';
import { ProBreadcrumb } from '@ant-design/pro-layout';
import { history } from 'core/mz';
import './style/index.less';
import { InitialState } from './types';

interface InitDate {
    initialState: InitialState;
}

export async function getInitialState() {
    if (history.location?.pathname === '/login') {
        return {};
    } else {
        // const { data } = await services.user.getUserInfo();
        // if (data === null) {
        //     history.replace('/login');
        // }
        // return {
        //     userId: data?.userId,
        //     userName: data?.userName
        // };
    }
}

export const layout = ({ initialState }: InitDate) => {
    return {
        headerBg: 'transparent',
        bodyBg: 'transparent',
        navTheme: 'light',
        layout: 'mix',
        title: '',
        siderWidth: 200,
        contentStyle: { padding: 0 },
        // 自定义页面标题的显示方法，浏览器选项卡显示的title信息
        pageTitleRender: () => 'Assistants',
        // 自定义产品Logo和文字
        logo: <HeaderLogo title={'Assistants'} />,
        // 自定义头部中间内容为面包屑导航
        headerContentRender: () => <ProBreadcrumb />,
        // 自定义头部导航右侧有关用户内容
        rightContentRender: () => <HeaderRight />
        // 验证用户身份
        // onPageChange: async () => {
        //     if (!initialState?.userId) {
        //         const user = await services.user.getUserInfo();
        //         if (!user) {
        //             history.push('/login');
        //             return;
        //         }
        //     }
        // }
    };
};

// 配置 request
export const request: RequestConfig = {
    baseURL: APIURL,
    validateStatus(status) {
        return status >= 200 && status < 300;
    },
    errorConfig: {
        errorHandler, // 自定义异常处理
        errorThrower
    },
    requestInterceptors: [
        (url, options) => {
            return {
                url,
                options: {
                    ...options,
                    headers: {
                        ...options.headers,
                        Authorization: 'Bearer ' + localStorage.getItem('myKey')
                    }
                }
            };
        }
    ],
    responseInterceptors: [
        adaptor,
        (response: AxiosResponse) => {
            const code = String(response?.data?.code || response?.status);
            if (code === '401' || code === '-4004') {
                console.log('error:登录失效或身份失效!');
                history.push('/login');
            }
            return response;
        }
    ]
};
