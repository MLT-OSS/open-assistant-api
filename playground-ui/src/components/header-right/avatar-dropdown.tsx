import { logout } from '@/services/user';
import { LogoutOutlined, SettingOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, Button, Menu, Popover, Space } from 'antd';
import { isFunction } from 'lodash';
import type { MenuInfo } from 'rc-menu/lib/interface';
import React, { useCallback, useEffect, useRef } from 'react';
import { history, useModel } from 'umi';
import styles from './index.less';
import { SettingKey } from './setting-key';

const AvatarDropdown: React.FC = () => {
    const { initialState, setInitialState } = useModel('@@initialState');

    const onMenuClickLogout = useCallback(
        async (event: MenuInfo) => {
            const { key } = event;
            const { code } = await logout();
            if (code === 200) {
                // 清空登录状态
                setInitialState(() => undefined);
                window.localStorage.clear();
                history.replace('/login');
            }
            return;
        },
        [setInitialState]
    );

    const placeholder = (
        <div className={styles.loginName}>
            <Avatar size="small" icon={<UserOutlined />} alt="avatar" />
        </div>
    );

    // todo houmenghao
    // if (!initialState) {
    //     return placeholder;
    // }

    // const { userId, userName } = initialState;
    // if (!userId || !userName) {
    //     return placeholder;
    // }

    const settingRef = useRef(null);
    const openSetting = () => {
        const { _showModal } = settingRef?.current || { _showModal: null };

        if (isFunction(_showModal)) {
            // @ts-ignore
            _showModal();
        }
    };
    useEffect(() => {
        if (localStorage.getItem('myKey') === null) {
            openSetting();
        }
    }, []);

    const menuHeaderDropdown = (
        <Menu className={styles.menu}>
            {/* <Menu.Divider /> */}
            <Menu.Item key="setting" onClick={openSetting} icon={<SettingOutlined />}>
                Setting Key
            </Menu.Item>
            <Menu.Item key="logout" onClick={onMenuClickLogout} icon={<LogoutOutlined />}>
                退出登录
            </Menu.Item>
        </Menu>
    );

    return (
        <>
            <Popover content={menuHeaderDropdown} placement="bottomRight">
                <Button type="text">
                    <Space className={styles.loginName}>
                        <Avatar size="small" icon={<UserOutlined />} alt="avatar" />
                        {/* {userName} */}
                        miaozhen
                    </Space>
                </Button>
            </Popover>
            <SettingKey ref={settingRef} />
        </>
    );
};

export default AvatarDropdown;
