/**
 * 自定义头部导航右侧有关用户内容
 */

import { Divider, Space } from 'antd';
import React from 'react';
import Avatar from './avatar-dropdown';

export type SiderTheme = 'light' | 'dark';

const GlobalHeaderRight: React.FC = () => {
    return (
        <Space split={<Divider type="vertical" />} size="small">
            <Avatar />
        </Space>
    );
};
export default GlobalHeaderRight;
