import services from '@/services';
import { CodeOutlined, CopyOutlined, DeleteOutlined, DownOutlined, EditOutlined } from '@ant-design/icons';
import ProTable, { ProColumns } from '@ant-design/pro-table';
import { Button } from 'antd';
import { history, useRequest } from 'core/mz';
import moment from 'moment';
import React, { forwardRef, useEffect, useImperativeHandle, useState } from 'react';
import style from './index.less';

interface Props {
    handleDelete: (id: string, content: string) => void;
    openDrawer: (e: any) => void;
}

const AssistantsTable = (props: Props, ref: any) => {
    const { handleDelete, openDrawer } = props;
    const [list, setList] = useState<any>([]);
    const [showNumber, setShowNumber] = useState<number>(0);
    const [hasMore, setHasMore] = useState<boolean>();
    const [afterAssistant, setAfterAssistant] = useState<any>('');

    useImperativeHandle(ref, () => {
        return {
            _refresh() {
                refresh();
            }
        };
    });
    // 创建/编辑/复制
    const showDrawer = (id: any, type: string, title: string) => {
        openDrawer({ id, type, title });
    };
    // 删除
    const onDelete = (id: string, name: string) => {
        handleDelete(id, `确定要删除 ${name} 吗？`);
    };

    // toPlayground
    const goPlayground = (assistant: string) => {
        history.push(`/playground/?id=${assistant}`);
    };

    const columns: ProColumns<any>[] = [
        {
            title: 'Name',
            dataIndex: 'name',
            align: 'center',
            width: 200,
            ellipsis: true
        },
        {
            title: 'Instructions',
            dataIndex: 'instructions',
            align: 'center',
            ellipsis: true
        },
        {
            title: 'ID',
            dataIndex: 'id',
            align: 'center',
            ellipsis: true
        },
        {
            title: 'Date Created',
            dataIndex: 'created_at',
            align: 'center',
            render: (dom, item) => {
                return <div>{moment(item.created_at * 1000).format('YYYY-MM-DD HH:mm:ss')}</div>;
            }
        },
        {
            title: '操作',
            dataIndex: 'operate',
            align: 'center',
            fixed: 'right',
            width: 200,
            render: (t: any, r: any) => {
                return (
                    <div>
                        <Button type="link" onClick={() => showDrawer(r.id, 'edit', '编辑')}>
                            <EditOutlined />
                        </Button>
                        <Button type="link" onClick={() => showDrawer(r.id, 'copy', '复制')}>
                            <CopyOutlined />
                        </Button>
                        <Button type="link" onClick={() => goPlayground(r.id)}>
                            <CodeOutlined />
                        </Button>
                        <Button type="link" danger onClick={() => onDelete(r.id, r.name)}>
                            <DeleteOutlined />
                        </Button>
                    </div>
                );
            }
        }
    ];

    useEffect(() => {
        if (!localStorage.getItem('myKey')) {
            setList([]);
            setHasMore(false);
            setShowNumber(0);
            setAfterAssistant('');
            return;
        }
        getAssistantsList();
    }, []);

    // 获取列表数据
    const getAssistantsList = () => {
        const params = afterAssistant ? { after: afterAssistant } : {};
        runAssistants({ limit: '10', ...params });
    };

    // 请求列表接口
    const { loading, run: runAssistants } = useRequest(services.assistants.getAssistantsList, {
        manual: true,
        onSuccess: (res) => {
            const { data, has_more, last_id } = res;
            setShowNumber(data.length + showNumber);
            setList([...list, ...data]);
            setHasMore(has_more);
            setAfterAssistant(last_id);
        }
    });

    // 重置,刷新列表
    const refresh = async () => {
        const list = await refreshList([], '', 0);
        setList(list);
    };
    // 递归刷新获取列表数据
    const refreshList: any = async (list: any, after: string, num: number) => {
        const params = after ? { after } : {};
        const res = await services.assistants.getAssistantsList({ limit: '10', ...params });
        const { data, has_more, last_id } = res.data;
        const count = num + data.length;
        const newList = [...list, ...data];
        if (has_more && count < showNumber) {
            return refreshList(newList, last_id, count);
        } else {
            setShowNumber(count);
            setHasMore(has_more);
            setAfterAssistant(last_id);
            return newList;
        }
    };

    // 底部加载更多
    const footerRender = () => {
        return (
            hasMore && (
                <div style={{ margin: -12 }}>
                    <Button size="small" type="link" onClick={getAssistantsList}>
                        <DownOutlined /> Load more
                    </Button>
                </div>
            )
        );
    };

    // 工具栏
    const toolBarRender = () => {
        return [
            <Button type="primary" key="add" onClick={() => showDrawer('', 'add', '新建')}>
                新建
            </Button>
        ];
    };
    return (
        <>
            <ProTable<any>
                className={style['assistants-table']}
                headerTitle="Assistants"
                options={false}
                search={false}
                rowKey="id"
                scroll={{ y: '100%' }}
                columns={columns}
                // loading={loading}
                dataSource={list}
                pagination={false}
                footer={footerRender}
                toolBarRender={toolBarRender}
            />
        </>
    );
};

export default forwardRef(AssistantsTable);
