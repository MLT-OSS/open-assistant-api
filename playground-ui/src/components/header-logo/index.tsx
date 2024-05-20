/**
 * 自定义产品Logo和文字
 */

import logo from '../../assets/logo.png';
import styles from './index.less';

const GlobalHeaderRight = (props: { title: string }) => {
    const { title } = props;
    return (
        <div className={styles.headerLogo}>
            {/* <LogoSvg /> */}
            <div>
                <img style={{ height: 42 }} src={logo} />
            </div>
            {/* <span className={styles.title}>{title}</span> */}
        </div>
    );
};
export default GlobalHeaderRight;
