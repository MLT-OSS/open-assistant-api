import { Col, Divider, Row } from 'antd';
import { useLocation } from 'core/mz';
import { isFunction } from 'lodash';
import React, { useEffect, useRef, useState } from 'react';
import { AssistantsFrom } from '../assistants/components/assistants-form';
import AssistantsFilter from './components/assistants-filter';
import Conversation from './components/conversation';
import style from './index.less';

interface Props {}
const myKey = localStorage.getItem('myKey');

const Playground: React.FC<Props> = () => {
    const { search } = useLocation();
    const [assistant, setAssistant] = useState<any>('');
    const [assistantName, setAssistantName] = useState<any>('');
    const [assistantType, setAssistantType] = useState<any>('');

    const searchParams = new URLSearchParams(search);
    const id = searchParams.get('id');
    // form表单最新数据
    useEffect(() => {
        if (myKey === null) return;
        setAssistant(id);
        setAssistantType(id === null ? 'new' : 'test');
    }, [id]);

    const modifyAssistant = (res: any) => {
        setAssistantName(res.name);
        resetRun();
    };
    const toSetTitle = (title: string) => {
        setAssistantName(title);
    };

    const conversationRef: any = useRef(null);
    const resetRun = () => {
        const { _resetRun } = conversationRef?.current || { _resetRun: null };

        if (isFunction(_resetRun)) {
            // @ts-ignore
            _resetRun();
        }
    };
    return (
        <div className={style.playground}>
            <Row>
                <Col span={8}>
                    <AssistantsFilter assistant={assistant} title={assistantName} />
                    <Divider />
                    <AssistantsFrom
                        id={assistant}
                        type={assistantType}
                        onSave={modifyAssistant}
                        toSetAssistantTitle={toSetTitle}
                    />
                </Col>

                <Col span={16} className="left-col-border">
                    <Conversation ref={conversationRef} assistant={assistant} />
                </Col>
            </Row>
        </div>
    );
};

export default Playground;
