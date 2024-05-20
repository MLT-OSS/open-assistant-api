import React from 'react';
import style from './index.less';

const MsgLoading: React.FC = () => {
    return (
        <div className={style.loadingContainer}>
            <div className={style.loadingDot} />
            <div className={style.loadingDot} />
            <div className={style.loadingDot} />
        </div>
    );
};
export default MsgLoading;
