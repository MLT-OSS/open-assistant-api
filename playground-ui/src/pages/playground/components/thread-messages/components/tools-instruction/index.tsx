import { isJson } from '@/utils/utils';
import { DownOutlined, UpOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import s from './index.less';

/**
 *  tools-instruction
 */
interface Props {
    content: any;
}
const ToolsInstruction = ({ content }: Props) => {
    const [expand, setExpand] = useState<boolean>(false);
    const [info, setInfo] = useState<any>([]);
    const [name, setName] = useState<any>('');
    useEffect(() => {
        if (!content) return;
        console.log(content);

        const name = content?.name;
        setName(name);
        if (!isJson(content?.output)) {
            return;
        }
        const output = JSON.parse(content?.output?.replace(/'/g, '"'));
        let info: any = [];
        let outputArr: any = [];
        // 判断output是否为对象
        if (typeof output === 'object') {
            outputArr = [output];
        }
        info = outputArr?.map((item: any) => {
            return Object.entries(item).map(([key, value]) => {
                let content = value;
                if (typeof value === 'object') {
                    content = JSON.stringify(value);
                }
                content += `<br/>`;
                return { title: key, content };
            });
        });
        console.log(info);

        setInfo(info);
        console.log(info);
    }, [content]);
    return (
        <div className={s['run-instructions']}>
            <div className={s['run-instructions-header']}>
                <div>Tools-{name}</div>
                <Button
                    type="text"
                    onClick={() => {
                        setExpand(!expand);
                    }}>
                    {expand ? <UpOutlined /> : <DownOutlined />}
                </Button>
            </div>
            <div className={expand ? s['instruction-content-expanded '] : s['instruction-content']}>
                {info.map((item: any, index: number) => {
                    return item.map((v: any, i: number) => {
                        return (
                            <div className={s['instruction-item']} key={i}>
                                <div className={s['instruction-item-title']}>
                                    {v.title}:<ReactMarkdown rehypePlugins={[rehypeRaw]}>{v.content}</ReactMarkdown>
                                </div>
                            </div>
                        );
                    });
                })}
            </div>
        </div>
    );
};
export default ToolsInstruction;
