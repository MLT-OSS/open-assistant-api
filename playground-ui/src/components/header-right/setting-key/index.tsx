import { Button, Input, Modal } from 'antd';
import { forwardRef, useImperativeHandle, useState } from 'react';

interface ModalProps {}

export const SettingKey = forwardRef((props: ModalProps, ref: any) => {
    const [delOpen, setDelOpen] = useState<boolean>(false);
    const [value, setValue] = useState<string>('');

    useImperativeHandle(ref, () => {
        return {
            _showModal() {
                setValue(localStorage.getItem('myKey') || '');
                setDelOpen(true);
            }
        };
    });

    const onValueChange = (e: any) => {
        setValue(e.target.value);
    };

    const onCancel = () => {
        setDelOpen(false);
    };

    const handleOnOk = () => {
        // 将value设置到localstorage中
        localStorage.setItem('myKey', value);
        setDelOpen(false);
    };

    const footerRender = () => {
        const confirm = (
            <Button disabled={!value} type="primary" key="link" onClick={handleOnOk}>
                确认
            </Button>
        );
        const cancel = (
            <Button key="cancel" onClick={onCancel}>
                取消
            </Button>
        );
        return localStorage.getItem('myKey') !== null ? [...[cancel], ...[confirm]] : [confirm];
    };

    return (
        <Modal
            centered
            width={368}
            title={<div style={{ textAlign: 'center' }}>Setting</div>}
            closeIcon={false}
            open={delOpen}
            zIndex={10002}
            onCancel={onCancel}
            destroyOnClose={true}
            keyboard={false}
            maskClosable={false}
            footer={footerRender}>
            <div>设定你的key值</div>
            <div style={{ marginTop: 12 }}>
                <Input placeholder="your key" value={value} onChange={onValueChange} />
            </div>
        </Modal>
    );
});
