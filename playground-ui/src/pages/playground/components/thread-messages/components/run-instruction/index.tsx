import { DownOutlined, UpOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import { useState } from 'react';
import s from './index.less';

/**
 *  run-instruction
 */
interface Props {
    content: string;
}
const RunInstruction = ({ content }: Props) => {
    const [expand, setExpand] = useState<boolean>(false);
    return (
        <div className={s['run-instructions']}>
            <div className={s['run-instructions-header']}>
                <div>Run instructions</div>
                <Button
                    type="text"
                    onClick={() => {
                        setExpand(!expand);
                    }}>
                    {expand ? <UpOutlined /> : <DownOutlined />}
                </Button>
            </div>
            <div className={expand ? s['instruction-content-expanded '] : s['instruction-content']}>{content}</div>
        </div>
    );
};
export default RunInstruction;
