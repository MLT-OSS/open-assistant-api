import React from 'react';
import JSONEditor from 'react-json-editor-ajrm';

function Index() {
    return (
        <div className="App">
            <JSONEditor
                // className="jsonEditor"
                colors={{
                    background: 'transparent' // 更改背景颜色为透明
                }}
                // viewOnly={false}
                // viewOnly={true} // 设置为只读模式
                confirmGood={false}
                width="100%"
                placeholder={{ name: 'John Doe', age: 30, city: 'New York' }}
            />
        </div>
    );
}

export default Index;
