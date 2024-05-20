import { CloseOutlined } from '@ant-design/icons';
import { Button, Divider, Drawer } from 'antd';
import { history } from 'core/mz';
import React, { forwardRef, useImperativeHandle, useState } from 'react';
import { AssistantsFrom } from '../assistants-form';
import style from './index.less';

interface assistantsProps {
    refresh: () => void;
}
export const AssistantsDrawer = forwardRef((props: assistantsProps, ref: any) => {
    const [drawerOpen, setDrawerOpen] = useState<boolean>(false);
    const [info, setInfo] = useState<any>({});

    const onSave = (data: any) => {
        setInfo({ type: 'edit', title: '编辑', id: data.id });
        props.refresh();
    };

    useImperativeHandle(ref, () => {
        return {
            _showDrawer(info: any) {
                setInfo(info);
                setDrawerOpen(true);
            }
        };
    });

    // 关闭抽屉
    const handleOnClose = () => {
        setDrawerOpen(false);
    };

    // 跳转playground页面
    const goPlayground = () => {
        history.push(`/playground/?id=${info.id}`);
    };
    return (
        <>
            <Drawer
                className={style['assistants-drawer']}
                title={false}
                extra={false}
                placement={'right'}
                closable={false}
                onClose={handleOnClose}
                open={drawerOpen}
                footer={false}
                key={'right'}>
                <div className="assistants-form-header">
                    <div className="bt-close">
                        <Button type="text" onClick={handleOnClose}>
                            <CloseOutlined />
                        </Button>
                        {info.title}
                    </div>
                    <div>
                        {(info.type === 'edit' && info.title === '编辑') || info.type === 'copy' ? (
                            <Button onClick={goPlayground}>Test</Button>
                        ) : null}
                    </div>
                </div>
                <Divider />
                <AssistantsFrom
                    onSave={onSave}
                    title={info.title}
                    id={info.id}
                    type={info.type}
                    onClose={handleOnClose}
                />
            </Drawer>
        </>
    );
});
