/**
 *  assistants列表和选择
 */
import services from '@/services';
import { PlusOutlined } from '@ant-design/icons';
import { Dropdown, Input } from 'antd';
import { useEffect, useState } from 'react';
import { history, useRequest } from 'umi';

const { TextArea } = Input;

interface Props {
    assistant?: string;
    title: string;
}

const item = [
    {
        label: (
            <a
                onClick={() => {
                    history.push(`/playground`);
                }}>
                <PlusOutlined /> Create assistant
            </a>
        ),
        key: '0'
    },
    {
        type: 'divider'
    }
];
const AssistantsFilter = ({ assistant, title }: Props) => {
    const [menuList, setMenuList] = useState<any>(item);
    useEffect(() => {
        if (!localStorage.getItem('myKey')) {
            toSetAssistantList([]);
            return;
        }
        runAssistants({ limit: '100' });
    }, [assistant]);

    // 获取助手列表
    const { loading, run: runAssistants } = useRequest(services.assistants.getAssistantsList, {
        manual: true,
        onSuccess: (res) => {
            toSetAssistantList(res.data);
        }
    });

    // 设定助手列表
    const toSetAssistantList = (list: any) => {
        const items = list.map((item: any) => {
            return {
                label: <a onClick={() => goPlayground(item.id)}>{item.name}</a>,
                key: item.id
            };
        });

        setMenuList([...item, ...items]);
    };

    // 跳转assistant playground
    const goPlayground = (id: any) => {
        history.push(`/playground?id=${id}`);
    };

    return (
        <div style={{ marginTop: 24, padding: '0 24px' }}>
            <Dropdown menu={{ items: menuList }} overlayStyle={{ maxHeight: '150px', overflow: 'auto' }}>
                {title ? <div>{title}</div> : <div>undefined</div>}
            </Dropdown>
        </div>
    );
};
export default AssistantsFilter;
