/**
 *  会话
 */
import services from '@/services';
import { isJson } from '@/utils/utils';
import { PaperClipOutlined } from '@ant-design/icons';
import { Button, Input, Upload } from 'antd';
import React, { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { useRequest } from 'umi';
import ThreadMessages from '../thread-messages';
import s from './index.less';
const { TextArea } = Input;

interface Props {
    assistant: string;
}

const Conversation = ({ assistant }: Props, ref: any) => {
    const [inputValue, setInputValue] = useState<any>('');
    const [addValue, setAddValue] = useState<any>('');
    const [lastMsgId, setLastMsgId] = useState<any>('');
    const [threadId, setThreadId] = useState<any>('');
    const [messagesList, setMessagesList] = useState<any>([]);

    const [runDisabled, setRunDisabled] = useState<any>(false);

    const [partialJson, setPartialJson] = useState<string>('');

    const [runInstructions, setRunInstructions] = useState<string>('');

    useImperativeHandle(ref, () => {
        return {
            _resetRun() {
                setRunInstructions('');
            }
        };
    });

    // 创建thread
    const { run: createThreads } = useRequest(services.threads.createThreads, {
        manual: true,
        onSuccess: (result: any) => {
            setThreadId(result.id);
        }
    });

    // 发送消息
    const { run: createMessages } = useRequest(services.threads.createMessages, { manual: true });

    // 获取message
    const { run: getMessagesList } = useRequest(services.threads.listMessages, {
        manual: true,
        onSuccess: (result: any) => {
            // setMessagesList(result);
        }
    });

    // 运行
    const run = async () => {
        setRunDisabled(true);
        // 创建thread
        let thread_id = threadId;
        if (!thread_id) {
            const thread: any = await createThreads({});
            thread_id = thread.id;
        }

        let last_msg_id = '';
        let message: any;
        if (inputValue || fileList.length > 0) {
            // 发送消息
            message = await createMessages(thread_id, {
                role: 'user',
                content: inputValue,
                file_ids: fileList.map((i: any) => i.response.id)
            });
            message.files = fileList.map((i: any) => {
                return { id: i.uid, name: i.name };
            });
            setMessagesList((prevMessages: any) => {
                return [...prevMessages, ...[message]];
            });
            // 获取message
            const list: any = await getMessagesList(thread_id, { limit: 100 });
            list.reverse(); // 反转数组的顺序
            last_msg_id = list[list.length - 1].id;
            setLastMsgId(last_msg_id);
            // 只含有文件没有文字,不执行run,直接返回
            if (list.length > 0 && !inputValue) {
                setFileList([]);
                setRunDisabled(false);
                return;
            }
            // 清空inputValue和fileList,避免重复发送
            setInputValue('');
            setFileList([]);
        }
        const addInstruction = addValue ? { additional_instructions: addValue } : {};
        runMsgStream(thread_id, { ...{ assistant_id: assistant }, ...addInstruction });
        singleRequestFlag.current = false;
        setRunDisabled(false);
    };

    // 轮循获取run下的setps,直到run的status === completed
    // 2秒轮循一次
    const timerRef = useRef<any>(null);
    const singleRequestFlag = useRef(true);

    // openapi适配 run stream获取结果
    const runMsgStream = async (thread_id: any, params: any) => {
        abortControllerRef?.current?.abort();
        const newAbortController = new AbortController();
        abortControllerRef.current = newAbortController;
        const url = `/api/v1/threads/${thread_id}/runs`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('myKey')
            },
            body: JSON.stringify({ ...params, stream: true }),
            signal: newAbortController?.signal || null
        });

        const reader = response?.body?.getReader();

        while (true) {
            const { done, value }: any = await reader?.read();
            console.log(done, value, 'done, value======');

            if (done) {
                break;
            }
            const decoder = new TextDecoder('utf-8');
            const chars = decoder.decode(value);
            const msg = getMsg(chars);
            console.log(msg, 'msg======');

            setMessagesList((prevMessages: any) => {
                // 如果messagesList不为空，更新最后一条消息
                const lastMessage = prevMessages[prevMessages.length - 1];
                if (lastMessage.role === 'assistant') {
                    lastMessage.content[0].text.value += msg;
                }
                return [...prevMessages];
            });
        }
    };

    const getMsg = (res: string) => {
        let c = '';
        const lines = res.replace(/\r/g, '').split('\n');
        const result: any = [];
        for (let i = 0; i < lines.length; i++) {
            if (lines[i] === '') continue;
            const event = lines[i].split('event: ')[1];
            console.log(event, 'event======');
            console.log(lines[i + 1], 'lines[i + 1]======');

            if (event) {
                const data = lines[i + 1].split('data: ')?.[1];
                result.push({ event, data });
            }
        }
        result?.forEach((items: any) => {
            if (!items.event) return;
            const { event, data } = items;
            if (isJson(data)) {
                const eventData = JSON.parse(data);
                console.log(
                    eventData.object,
                    eventData.object === 'thread.run',
                    'eventData.object === thread.run======'
                );
                // console.log(event === 'thread.run.created', event, 'event === thread.run.created======');

                // instructions展示
                if (event === 'thread.run.created') {
                    console.log(eventData, ' instructions展示======');

                    if (eventData.instructions !== runInstructions) {
                        setMessagesList((prevMessages: any) => {
                            return [...prevMessages, ...[{ role: 'run', content: eventData.instructions }]];
                        });
                        setRunInstructions(eventData.instructions);
                    }
                    return;
                }
                // tools展示
                if (eventData.object === 'thread.run.step') {
                    const detail = eventData?.step_details?.tool_calls?.[0].function;
                    if (detail?.output) {
                        setMessagesList((prevMessages: any) => {
                            return [...prevMessages, ...[{ role: 'tools', content: detail }]];
                        });
                    }
                    return;
                }
                if (event === 'thread.message.created') {
                    setMessagesList((prevMessages: any) => {
                        return [...prevMessages, ...[{ role: 'assistant', content: [{ text: { value: '' } }] }]];
                    });
                }
                if (event === 'thread.message.delta') {
                    const content = JSON.parse(data)?.delta?.content?.[0]?.text?.value;
                    c += content;
                    // console.log(c, 'c======');
                }
            }
        });
        return c;
    };

    useEffect(() => {
        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, []); // 注意这里的依赖数组为空，这意味着清理函数只会在组件卸载时运行

    const clear = () => {
        setThreadId('');
        setMessagesList([]);
        setRunInstructions('');
    };

    const content = (
        <div>
            <p style={{ color: '#6e6e80' }}>Use to provide additional context to assistant.</p>
            <TextArea
                value={addValue}
                onChange={(e) => setAddValue(e.target.value)}
                placeholder="eg. this user likes cats"
                autoSize={{ minRows: 3, maxRows: 5 }}
            />
        </div>
    );

    const abortControllerRef = useRef<AbortController>();

    const [fileList, setFileList] = useState<any>([]);

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
            }
        },
        action: '/api/v1/files'
    };
    const hiddenButtonRef = React.useRef<HTMLButtonElement>(null);

    const handleVisibleButtonClick = () => {
        if (hiddenButtonRef.current) {
            hiddenButtonRef.current.click();
        }
    };

    return (
        <div className={s.conversation}>
            <div className="assistants-pg-header">
                <div style={{ flex: '1 1' }}>
                    <span>THREAD</span>
                    <span className="ml-8">{threadId}</span>
                </div>

                {/* <Button className="ml-8">Cancel run</Button> */}
                <Button className="ml-8" onClick={clear}>
                    Clear
                </Button>
            </div>
            <div className="playground-drop-target">
                <ThreadMessages list={messagesList} />
                <div className="add-message-wrapper">
                    <div className="user-input">
                        <TextArea
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Enter your message..."
                            bordered={false}
                            autoSize={{ minRows: 3, maxRows: 5 }}
                        />

                        <div className="upload-list">
                            <Upload {...uploadProps} style={{ width: '50%' }}>
                                <Button ref={hiddenButtonRef} style={{ display: 'none' }} />
                            </Upload>
                        </div>

                        <div className="input-button-group">
                            <Button onClick={handleVisibleButtonClick}>
                                <PaperClipOutlined />
                            </Button>
                            <div />
                            <div style={{ display: 'flex' }}>
                                {/* <Button className="run" onClick={test2}>
                                    Run
                                </Button> */}
                                <Button
                                    style={{ background: '#10a37f' }}
                                    onClick={run}
                                    loading={runDisabled}
                                    disabled={!assistant || (runDisabled && fileList.length === 0)}>
                                    Run
                                </Button>
                                {/* <Popover content={content} title="Add run instructions" trigger="click">
                                    <Button className="add-instruction">
                                        <CaretDownOutlined />
                                    </Button>
                                </Popover> */}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default forwardRef(Conversation);
