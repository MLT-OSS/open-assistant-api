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
    // 1.创建一个新的thread
    // 2.携带threadId发起message
    // 3.获取thread的all-message
    // 4.携带threadId发起runs 获取run_id
    // 5.携带threadId,run_id获取steps
    // 6.判断run_steps status === completed/is_progress
    // 7.携带threadId,before-msgId获取run下的message
    // 重复 6-7  直到run的status === completed 获取all-message
    // 8.status === completed 时，获取run的result
    // 9.获取runs的steps是否都是completed

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

    // 创建run
    const { run: createRun } = useRequest(services.threads.createRuns, { manual: true });
    // 获取run下的steps
    const { run: getRunsSteps } = useRequest(services.threads.getRunsSteps, { manual: true });

    // 根据steps获取run下message
    const getRunMessages = (thread_id: string, before: string) => {
        runMessagesList(thread_id, { before, limit: 10 });
    };

    const { run: runMessagesList } = useRequest(services.threads.listMessages, {
        manual: true,
        onSuccess: (result: any) => {
            if (result.length > 0) {
                setMessagesList((prevMessages: any) => {
                    // 修改最后一条的date
                    const lastMessage = prevMessages[prevMessages.length - 1];
                    lastMessage.created_at = result[0].created_at;
                    return [...prevMessages];
                    // 最后一条记录
                    // return [...prevMessages, ...result];
                });
                // 等待
                setTimeout(() => {
                    singleRequestFlag.current = true;
                }, 1000);
            }
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
        // 创建run
        const run: any = await createRun(thread_id, { ...{ assistant_id: assistant }, ...addInstruction });

        if (run.instructions !== runInstructions) {
            setMessagesList((prevMessages: any) => {
                return [...prevMessages, ...[{ role: 'run', content: run.instructions }]];
            });
            setRunInstructions(run.instructions);
        }
        // 设定loading
        setMessagesList((prevMessages: any) => {
            return [...prevMessages, ...[{ role: 'loading' }]];
        });

        const run_id = run.id;
        roundRunSteps(thread_id, run_id, last_msg_id);
    };

    // 轮循获取run下的setps,直到run的status === completed
    // 2秒轮循一次
    const timerRef = useRef<any>(null);
    const singleRequestFlag = useRef(true);

    // 移除messageList中role为loading的数据
    const cancelLoading = () => {
        setMessagesList((prevMessages: any) => {
            const newList = prevMessages.filter((item: any) => {
                return item.role !== 'loading';
            });
            return [...newList];
        });
    };
    // 轮循获取run下的setps,直到run的status === completed
    const roundRunSteps = (thread_id: string, run_id: string, last_msg_id: string) => {
        let stepToolsId = '';
        timerRef.current = setInterval(async () => {
            const data: any = await getRunsSteps(thread_id, run_id, {});
            // data 顺序颠倒
            data.reverse();
            data.forEach((step: any) => {
                if (step && step?.type === 'tool_calls' && step?.status === 'completed' && step?.id !== stepToolsId) {
                    stepToolsId = step.id;
                    const detail = step?.step_details?.tool_calls[0].function;
                    cancelLoading();
                    setMessagesList((prevMessages: any) => {
                        return [...prevMessages, ...[{ role: 'tools', content: detail }]];
                    });
                }
                // 拿到message_creation的step 流式状况下去取消loading
                if (step && step?.type === 'message_creation') {
                    cancelLoading();
                }
                if ((step?.status === 'completed' && step?.type === 'message_creation') || step?.status === 'failed') {
                    cancelLoading();
                    setRunDisabled(false);
                    clearInterval(timerRef.current);
                    if (step?.status === 'failed') {
                        setMessagesList((prevMessages: any) => {
                            return [...prevMessages, ...[{ role: 'error' }]];
                        });
                    }
                }
                // 流式获取
                if (step && step?.type === 'message_creation' && singleRequestFlag.current) {
                    setMessagesList((prevMessages: any) => {
                        return [...prevMessages, ...[{ role: 'assistant', content: [{ text: { value: '' } }] }]];
                    });
                    getFetch(thread_id, run_id);
                    singleRequestFlag.current = false;
                }
            });
            if (data) getRunMessages(thread_id, last_msg_id);
        }, 2000);
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

    const getFetch = async (t: any, r: any) => {
        abortControllerRef?.current?.abort();

        const newAbortController = new AbortController();
        abortControllerRef.current = newAbortController;

        // const url = `http://10.10.10.12:30087/api/v1/threads/${t}/runs/${r}/stream`;
        const url = `/api/v1/threads/${t}/runs/${r}/stream`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + localStorage.getItem('myKey')
            },
            signal: newAbortController?.signal || null
        });

        const reader = response?.body?.getReader();

        while (true) {
            const { done, value }: any = await reader?.read();

            if (done) {
                break;
            }

            const decoder = new TextDecoder('utf-8');
            const chars = decoder.decode(value);

            const msg = getMsg(chars);
            // console.log(msg, 'msg======');

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
        const dataArray = res.trim().split('\n\n');
        let c = '';
        // console.log(dataArray, 'dataArray======');

        dataArray.forEach((data) => {
            const newData = partialJson + data;
            const event = newData.substring('data: '.length).replace(/\n/g, '');
            // console.log(data, 'event======');
            if (event === '') return;
            if (event === '[DONE]') {
                return;
            }
            if (!isJson(event)) {
                setPartialJson(() => {
                    return event;
                });
                return;
            }
            if (isJson(event)) {
                const content = JSON.parse(event)?.choices?.[0]?.delta?.content;
                // console.log(content, 'content======');
                c += content;
            }
        });
        return c;
    };
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
