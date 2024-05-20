import { Button, Result } from 'antd';
import React from 'react';
import './error-fallback.less';

interface ErrorFallbackProps {
    errorInfo?: string;
    error?: any;
}

const ErrorFallback: React.FC<ErrorFallbackProps> = ({ error, errorInfo }) => {
    return (
        <Result
            status="500"
            title="500"
            subTitle="Sorry, something went wrong."
            extra={
                <Button
                    danger
                    type="primary"
                    onClick={() => {
                        window.location.reload();
                    }}>
                    刷新页面
                </Button>
            }
        />
    );
};

export default ErrorFallback;
