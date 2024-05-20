import services from '@/services';
import { isJson } from '@/utils/utils';
import { Button, Drawer, Form, Input, message, Radio, Space, Switch } from 'antd';
import { useRequest } from 'core/mz';
import { forwardRef, useEffect, useImperativeHandle, useState } from 'react';

interface Props {
    refresh?: () => void; // 点击保存
}

export const ActionsDrawer = forwardRef((props: Props, ref: any) => {
    const [drawerOpen, setDrawerOpen] = useState<boolean>(false);
    const [info, setInfo] = useState<any>({});
    const [radioValue, setRadioValue] = useState('none');

    useImperativeHandle(ref, () => {
        return {
            _showDrawer(info: any) {
                setInfo(info);
                setDrawerOpen(true);
            }
        };
    });
    useEffect(() => {
        if (info.id) {
            runDetail(info.id);
        } else {
            form.resetFields(['openapi_schema', 'schema', 'content-key', 'content-val', 'secret']);
            form.setFieldsValue({ authentication: '1', type: 'none' });
            setRadioValue('none');
        }
    }, [info]);

    // 请求详情接口
    const { loading: detailLoading, run: runDetail } = useRequest(services.actions.get, {
        manual: true,
        onSuccess: (res) => {
            form.setFieldsValue({
                authentication: '1',
                type: res.authentication.type,
                schema: JSON.stringify(res.openapi_schema, null, 2),
                openapi_schema: JSON.stringify(res.openapi_schema, null, 2),
                use_for_everyone: res.use_for_everyone
            });
            setRadioValue(res.authentication.type);
            if (res.authentication.secret) {
                form.setFieldsValue({ secret: res.authentication.secret });
            }
            if (res.authentication.content) {
                form.setFieldsValue({
                    'content-key': Object.keys(res.authentication.content)[0],
                    'content-val': Object.values(res.authentication.content)[0]
                });
            }
        }
    });

    // 关闭抽屉
    const onClose = () => {
        setRadioValue('none');
        setDrawerOpen(false);
    };

    const [form] = Form.useForm();

    const [height, setHeight] = useState(`${window.innerHeight - 600}px`);

    useEffect(() => {
        const handleResize = () => {
            setHeight(`${window.innerHeight - 600}px`); // 200 是 Drawer 的标题和其他元素的总高度
        };

        window.addEventListener('resize', handleResize);

        // 在组件卸载时移除事件监听器
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const handleRadioChange = (e: any) => {
        setRadioValue(e.target.value);
        form.resetFields(['content', 'secret']);
    };

    const options = [
        { label: 'none', value: 'none' },
        { label: 'basic', value: 'basic' },
        { label: 'bearer', value: 'bearer' },
        { label: 'custom', value: 'custom' }
    ];

    const handleSave = () => {
        // 刷新当前页面
        form.validateFields().then((values) => {
            if (!isJson(values.schema)) {
                return message.error('Schema must be a valid JSON');
            }
            const authentication: any = { type: values.type };
            switch (values.type) {
                case 'basic':
                case 'bearer':
                    authentication['secret'] = values.secret;
                    break;
                case 'custom':
                    authentication['content'] = { [values['content-key']]: values['content-val'] };
                    break;
            }
            const value = {
                openapi_schema: JSON.parse(values.schema),
                authentication,
                use_for_everyone: values.use_for_everyone
            };
            if (info.id) {
                updateAction(info.id, value);
            } else {
                createAction(value);
            }
        });
    };

    // 保存action
    const { loading, run: createAction } = useRequest(services.actions.create, {
        manual: true,
        onSuccess: (res) => {
            message.success('新建成功');
            props.refresh?.(); // 点击保存
            onClose();
        }
    });
    // 更新
    const { loading: upLoading, run: updateAction } = useRequest(services.actions.update, {
        manual: true,
        onSuccess: (res) => {
            message.success('修改成功');
            props.refresh?.(); // 点击保存
            onClose();
        }
    });

    const onChange = (e: any) => {
        form.setFieldsValue({ schema: e.target.value });
    };

    const schemaDesc =
        'The action JSON schema is compliant with the OpenAPI Specification. If there are multiple paths and methods in the schema, the service will create multiple actions whose schema only has exactly one path and one method. We’ll use "operationId" and "description" fields ofeach endpoint method as the name and description of the tool. Check the documentation tolearn more.';

    const ruleRequired = [{ required: true, message: ' ' }];

    return (
        <>
            <Drawer
                title={(info.type === 'edit' ? 'Edit' : 'Create') + ' Actions'}
                onClose={onClose}
                open={drawerOpen}
                width={720}>
                <Form form={form} name="validateOnly" layout="vertical" autoComplete="off">
                    <Form.Item name="schema" label="Schema" rules={ruleRequired}>
                        <p style={{ color: 'gray' }}>{schemaDesc}</p>
                        <Form.Item name="openapi_schema" rules={ruleRequired}>
                            <Input.TextArea style={{ height }} onChange={onChange} />
                        </Form.Item>
                    </Form.Item>
                    <Form.Item name="authentication" label="Authentication" rules={ruleRequired}>
                        <p style={{ color: 'gray' }}>Authentication Type</p>
                        <Form.Item name="type" noStyle>
                            <Radio.Group options={options} onChange={handleRadioChange} value={radioValue} />
                        </Form.Item>
                    </Form.Item>
                    {(radioValue === 'basic' || radioValue === 'bearer') && (
                        <Form.Item>
                            <Space>
                                <p style={{ color: 'gray' }}>Authorization: </p>
                                <Form.Item name="secret" noStyle rules={ruleRequired}>
                                    <Input prefix={radioValue + ':'} placeholder="<Secret>" />
                                </Form.Item>
                            </Space>
                        </Form.Item>
                    )}

                    {radioValue === 'custom' && (
                        <Form.Item>
                            <Space>
                                <Form.Item name="content-key" noStyle rules={ruleRequired}>
                                    <Input placeholder="X-Custom" />
                                </Form.Item>
                                <Form.Item name="content-val" noStyle rules={ruleRequired}>
                                    <Input placeholder="<Secret>" />
                                </Form.Item>
                            </Space>
                        </Form.Item>
                    )}

                    <Form.Item name="use_for_everyone" label="使用全局Authentication" rules={ruleRequired}>
                        <Switch />
                    </Form.Item>

                    <Form.Item style={{ width: '100%' }}>
                        <Space style={{ float: 'right' }}>
                            <Button onClick={onClose}>取消</Button>
                            <Button type="primary" onClick={handleSave}>
                                保存
                            </Button>
                        </Space>
                    </Form.Item>
                </Form>
            </Drawer>
        </>
    );
});
