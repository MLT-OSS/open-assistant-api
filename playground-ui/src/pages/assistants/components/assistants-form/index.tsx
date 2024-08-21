import services from '@/services';
import { PaperClipOutlined, PlusCircleOutlined } from '@ant-design/icons';
import { Button, Col, Form, Input, message, Row, Select, Switch, Upload } from 'antd';
import { forEach, isEmpty, map } from 'lodash';
import React, { useEffect, useState } from 'react';
import { history, useRequest } from 'umi';
import style from './index.less';

const { TextArea } = Input;
const { Option } = Select;
const modelList = [
    { label: 'gpt-4', value: 'gpt-4' },
    { label: 'gpt-4-1106-preview', value: 'gpt-4-1106-preview' },
    { label: 'gpt-4o', value: 'gpt-4o' },
    { label: 'gpt-3.5-turbo-16k', value: 'gpt-3.5-turbo-16k' },
    { label: 'gpt-3.5-turbo-1106', value: 'gpt-3.5-turbo-1106' },
    { label: 'gpt-3.5-turbo', value: 'gpt-3.5-turbo' },
    { label: 'gemini-pro', value: 'gemini-pro' },
    { label: 'moonshot-v1-32k', value: 'moonshot-v1-32k' },
    { label: 'moonshot-v1-8k', value: 'moonshot-v1-8k' },
    { label: 'moonshot-v1-128k', value: 'moonshot-v1-128k' }
];
interface FormProps {
    id?: string; // id
    type?: string; // 'add'/"edit"/"copy"
    title?: string; // 名称
    onSave?: (data: any) => void; // 点击保存
    onClose?: () => void; // 点击关闭
    formData?: any; // 表单数据
    toSetAssistantTitle?: (title: any) => void; // 设置assistant标题
}
export const AssistantsFrom = (props: FormProps) => {
    const [form] = Form.useForm();
    const { title, id, type, onSave, onClose } = props;
    const [isShowButton, setIsShowButton] = useState(false);
    const [fileList, setFileList] = useState<any>([]);
    const [formData, setFormData] = React.useState<any>({});

    const [actionsList, setActionsList] = useState<any>([]);

    useEffect(() => {
        runActionList({ limit: '100' });
    }, []);
    // 获取actions
    const { loading, run: runActionList } = useRequest(services.actions.getList, {
        manual: true,
        onSuccess: (res) => {
            setActionsList(res.data);
        }
    });

    // 点击保存
    const handleSave = () => {
        // 刷新当前页面
        form.validateFields().then((values) => {
            const val = [
                { key: 'code_interpreter', val: !!values.code },
                { key: 'file_search', val: !!values.file_search },
                { key: 'web_search', val: !!values.search }
            ];
            const tools = val
                .filter((i) => i.val)
                .map((i) => {
                    return { type: i.key };
                });
            let actions = [];
            if (values.actions) {
                actions = values.actions.map((i: any) => {
                    return { id: i, type: 'action' };
                });
            }
            tools.push(...actions);
            values.tools = tools.length > 0 ? tools : [];
            switch (type) {
                case 'add':
                case 'copy':
                case 'new':
                    runAddAssistants(values);
                    break;
                case 'edit':
                case 'test':
                    runEditAssistants({ ...values, assistant_id: id });
                    break;
            }
        });
    };
    // 上传
    const uploadProps = {
        fileList,
        multiple: true,
        onChange: (res: any) => {
            setFileList(res.fileList);
            if (res.fileList.every((i: any) => i.status === 'done')) {
                const arr = res.fileList.map((i: any) => {
                    if (i.response) return i.response;
                    return i;
                });
                form.setFieldValue(
                    'file_ids',
                    arr.map((i: any) => i.id)
                );
            }
        },
        action: '/api/v1/files'
    };
    // 监听form变化
    const handelValueChange = (changedValues: any, allValues: any) => {
        setIsShowButton(true);
    };
    // 请求新建接口
    const { loading: addAssistantsLoading, run: runAddAssistants } = useRequest(services.assistants.addAssistants, {
        manual: true,
        onSuccess: (res) => {
            if (!isEmpty(res?.id)) {
                message.success('新建成功');
                setIsShowButton(false);
                // 刷新当前页
                if (type === 'new') {
                    history.push(`/playground?id=${res.id}`);
                } else {
                    onSave?.(res);
                }
            }
        }
    });
    // 请求编辑接口
    const { loading: editAssistantsLoading, run: runEditAssistants } = useRequest(services.assistants.editAssistants, {
        manual: true,
        onSuccess: (res) => {
            if (!isEmpty(res?.id)) {
                message.success('编辑成功');
                setIsShowButton(false);
                onSave?.(res);
            }
        }
    });
    // 请求详情接口
    const { loading: AssistantsDetailLoading, run: runAssistantsDetail } = useRequest(
        services.assistants.assistantsDetail,
        {
            manual: true,
            onSuccess: (res) => {
                let code;
                let file_search;
                let search;
                const actions = [];
                if (res && !isEmpty(res?.tools)) {
                    forEach(res?.tools, (item: any) => {
                        // eslint-disable-next-line @typescript-eslint/no-unused-expressions
                        switch (item.type) {
                            case 'code_interpreter':
                                code = true;
                                break;
                            case 'file_search':
                                file_search = true;
                                break;
                            case 'web_search':
                                search = true;
                                break;
                            case 'action':
                                actions.push(item.id);
                                break;
                        }
                        // item.type === 'code_interpreter'
                        //     ? (code = true)
                        //     : item.type === 'file_search'
                        //     ? (file_search = true)
                        //     : item.type === 'web_search'
                        //     ? (search = true)
                        //     : undefined;
                    });
                }
                form.resetFields();
                form.setFieldsValue({ ...res, ...{ code, file_search, search, file_ids: res.file_ids, actions } });
                if (!isEmpty(res?.file_ids)) {
                    runFileName({
                        ids: res.file_ids
                    });
                } else {
                    setFileList([]);
                }
                props.toSetAssistantTitle?.(res.name);
            }
        }
    );

    // 请求文件回显接口
    const { loading: fileLoading, run: runFileName } = useRequest(services.assistants.getFileName, {
        manual: true,
        onSuccess: (res) => {
            const arr = map(res, (i: any) => {
                return {
                    id: i.id,
                    name: i.filename,
                    status: 'done'
                };
            });
            setFileList(arr);
            form.setFieldValue(
                'file_ids',
                arr.map((i: any) => i.id)
            );
        }
    });
    useEffect(() => {
        setIsShowButton(false);
        if (type !== 'add' && id) {
            runAssistantsDetail({
                assistant_id: id!
            });
        }
        if (type === 'add' || type === 'new') {
            props.toSetAssistantTitle?.(undefined);
            form.resetFields();
            setFileList([]);
        }
    }, [id]);
    return (
        <>
            <Form
                className={style['assistants-form']}
                form={form}
                initialValues={{ code: false, file_search: false, fileIds: [] }}
                onValuesChange={handelValueChange}>
                <div className="assistants-form-body">
                    <Row>
                        <Col span={24}>
                            <Form.Item labelCol={{ span: 24 }} wrapperCol={{ span: 24 }} label="Name" name="name">
                                <Input />
                            </Form.Item>
                        </Col>
                    </Row>
                    <Row>
                        <Col span={24}>
                            <Form.Item
                                labelCol={{ span: 24 }}
                                wrapperCol={{ span: 24 }}
                                label="Instructions"
                                name="instructions">
                                <TextArea style={{ height: 110, resize: 'none' }} />
                            </Form.Item>
                        </Col>
                    </Row>
                    <Row>
                        <Col span={24}>
                            <Form.Item labelCol={{ span: 24 }} wrapperCol={{ span: 24 }} label="Model" name="model">
                                <Select>
                                    {map(modelList, (item) => {
                                        return (
                                            <Option key={`${item.value}${item.label}`} value={item.value}>
                                                {item.label}
                                            </Option>
                                        );
                                    })}
                                </Select>
                            </Form.Item>
                        </Col>
                    </Row>

                    <Form.Item
                        label="Functions"
                        labelCol={{ span: 16 }}
                        wrapperCol={{ span: 8 }}
                        labelAlign="left"
                        name="function">
                        <Button disabled type="text" className="function-button">
                            <PlusCircleOutlined />
                            Add
                        </Button>
                    </Form.Item>

                    <Form.Item
                        valuePropName="checked"
                        label="Code interpreter"
                        labelCol={{ span: 16 }}
                        wrapperCol={{ span: 8 }}
                        labelAlign="left"
                        name="code">
                        <Switch disabled className="code-button" />
                    </Form.Item>

                    <Form.Item
                        valuePropName="checked"
                        label="File Search"
                        labelCol={{ span: 16 }}
                        wrapperCol={{ span: 8 }}
                        labelAlign="left"
                        name="file_search">
                        <Switch className="code-button" />
                    </Form.Item>

                    <Form.Item
                        valuePropName="checked"
                        label="Web search"
                        labelCol={{ span: 16 }}
                        wrapperCol={{ span: 8 }}
                        labelAlign="left"
                        name="search">
                        <Switch className="code-button" />
                    </Form.Item>

                    <Row>
                        <Col span={24}>
                            <Form.Item labelCol={{ span: 24 }} wrapperCol={{ span: 24 }} label="Actions" name="actions">
                                <Select mode="multiple" placeholder="选择Tools Actions">
                                    {map(actionsList, (item) => {
                                        return (
                                            <Option key={item.id} value={item.id}>
                                                {item.description}
                                            </Option>
                                        );
                                    })}
                                </Select>
                            </Form.Item>
                        </Col>
                    </Row>

                    <Form.Item
                        className="form-style"
                        label="FILES"
                        labelCol={{ span: 14 }}
                        wrapperCol={{ span: 10 }}
                        labelAlign="left"
                        name="file_ids">
                        <Upload {...uploadProps} className="files-button">
                            <Button type="text">
                                <PaperClipOutlined />
                                Add
                            </Button>
                        </Upload>
                    </Form.Item>
                </div>
                {isShowButton && (
                    <div className="footer-button">
                        {(type === 'edit' && title !== '编辑') ||
                            (type !== 'test' && (
                                <Button className="footer-button-cancel" onClick={onClose}>
                                    Revert changes
                                </Button>
                            ))}
                        <Button type="primary" className="footer-button-save" onClick={handleSave}>
                            Save
                        </Button>
                    </div>
                )}
            </Form>
        </>
    );
};
