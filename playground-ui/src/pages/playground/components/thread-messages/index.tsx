/**
 *  会话
 */
import { Input, Upload } from 'antd';
import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';
import ErrorMsg from './components/error-msg';
import MsgLoading from './components/msg-loading';
import RunInstruction from './components/run-instruction';
import ToolsInstruction from './components/tools-instruction';
import s from './index.less';

const { TextArea } = Input;

interface Props {
    list: any[];
}
const ThreadMessages = ({ list }: Props) => {
    const endRef = useRef(null);
    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [list]);

    return (
        <div className={s['thread-messages']}>
            <div className="thread-detail">
                {list?.map((item, index) => {
                    return (
                        <div className="thread-item" key={index}>
                            {(item.role === 'user' || item.role === 'assistant') && (
                                <div className="thread-item-header">
                                    <span>
                                        <div className="thread-item-header-author">{item.role}</div>
                                    </span>
                                </div>
                            )}
                            {item.role === 'tools' && <ToolsInstruction content={item.content} />}
                            {item.role === 'run' && <RunInstruction content={item.content} />}
                            {item.role === 'loading' && <MsgLoading />}
                            {item.role === 'error' && <ErrorMsg />}

                            {(item.role === 'user' || item.role === 'assistant') && (
                                <div className="thread-content">
                                    <div>
                                        <ReactMarkdown remarkPlugins={[gfm]}>
                                            {item.content[0].text.value}
                                        </ReactMarkdown>
                                    </div>
                                    <div>
                                        {item.file_ids && item.file_ids.length > 0 && (
                                            <Upload
                                                listType="text"
                                                defaultFileList={[...item.files]}
                                                showUploadList={{
                                                    showRemoveIcon: false
                                                }}
                                            />
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
            <div ref={endRef} />
        </div>
    );
};
export default ThreadMessages;
