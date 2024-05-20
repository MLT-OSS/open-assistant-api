import { isFunction } from 'lodash';
import React, { useRef } from 'react';
import { AssistantsDrawer } from './components/assistants-drawer';
import AssistantsTable from './components/assistants-table';
import { DeleteModal } from './components/delete-modal';
import style from './index.less';

interface AssistantsProps {}

const Assistants: React.FC<AssistantsProps> = () => {
    const deleteModalRef = useRef(null);
    const assistantsDrawerRef = useRef(null);
    const tableRef = useRef(null);

    // 删除
    const handleDelete = (id: string, content: string) => {
        const { _showModal } = deleteModalRef?.current || { _showModal: null };

        if (isFunction(_showModal)) {
            // @ts-ignore
            _showModal(id, content);
        }
    };

    // 打开抽屉, 修改/编辑/删除
    const openDrawer = (info: any) => {
        const { _showDrawer } = assistantsDrawerRef?.current || { _showDrawer: null };

        if (isFunction(_showDrawer)) {
            // @ts-ignore
            _showDrawer(info);
        }
    };

    // 刷新
    const refresh = () => {
        const { _refresh } = tableRef?.current || { _refresh: null };

        if (isFunction(_refresh)) {
            // @ts-ignore
            _refresh();
        }
    };
    return (
        <div className={style.assistants}>
            <AssistantsTable ref={tableRef} handleDelete={handleDelete} openDrawer={openDrawer} />
            <AssistantsDrawer ref={assistantsDrawerRef} refresh={refresh} />
            <DeleteModal ref={deleteModalRef} refresh={refresh} />
        </div>
    );
};

export default Assistants;
