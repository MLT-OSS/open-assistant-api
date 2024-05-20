/**
 * 删除二次确认弹窗
 */
import services from '@/services';
import { Button, message, Modal } from 'antd';
import { forwardRef, useImperativeHandle, useState } from 'react';
import { useRequest } from 'umi';
import styles from './index.module.less';

interface IDeleteModalProps {
    refresh: () => void;
}

export const DeleteModal = forwardRef((props: IDeleteModalProps, ref: any) => {
    const [delOpen, setDelOpen] = useState<boolean>(false);
    const [content, setContent] = useState<string>('');
    const [delId, setDelId] = useState<string>('');

    useImperativeHandle(ref, () => {
        return {
            _showModal(id: string, content: string) {
                setDelId(id);
                setContent(content);
                setDelOpen(true);
            }
        };
    });

    // 确认删除
    const handleOnOk = () => {
        if (delId) {
            del(delId);
        }
    };
    // 请求删除接口
    const { loading: deleteLoading, run: del } = useRequest(services.actions.del, {
        manual: true,
        onSuccess: (res) => {
            if (res?.deleted) {
                message.success('删除成功');
                setDelOpen(false);
                props.refresh();
            }
        }
    });

    // 取消
    const onCancel = () => {
        setDelOpen(false);
    };

    return (
        <Modal
            wrapClassName={styles['delete-modal']}
            centered
            width={368}
            title={<div style={{ textAlign: 'center' }}>删除</div>}
            closeIcon={false}
            open={delOpen}
            zIndex={10002}
            onCancel={onCancel}
            destroyOnClose={true}
            footer={[
                <Button className={styles.cancel} key="cancel" onClick={onCancel}>
                    取消
                </Button>,
                <Button className={styles.save} loading={deleteLoading} type="primary" key="link" onClick={handleOnOk}>
                    确认
                </Button>
            ]}>
            <div className="content">{content}</div>
        </Modal>
    );
});
