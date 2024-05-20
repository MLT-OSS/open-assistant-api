import services from '@/services';
import { InitialState } from '@/types';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Form, Input, Layout } from 'antd';
import { history, useModel, useRequest } from 'core/mz';
import styles from './login.less';
export interface LoginProps {}

const { Content } = Layout;

const Login: React.FC<LoginProps> = (props) => {
    const { initialState, setInitialState } = useModel('@@initialState');
    const { run, loading: loginLoading } = useRequest(services.user.login, {
        manual: true,
        onSuccess: (user) => {
            const initData: InitialState = {
                ...initialState,
                userName: user.userName,
                userId: user.userId
            };
            setInitialState(initData);
            history.push('/dashboard');
        }
    });

    const handleSubmit = (value: { username: string; password: string }) => {
        history.push('/playground');
        // run({ username: value.username, password: value.password });
    };

    return (
        <Layout className={styles.loginContainer}>
            <Content className={styles.formContainer}>
                <div className={styles.title}>欢迎登录</div>
                <Form onFinish={handleSubmit}>
                    <Form.Item
                        name="username"
                        validateTrigger={['onBlur']}
                        rules={[
                            // { type: 'email', message: '请输入正确的邮箱' },
                            { required: true, message: '请输入用户名' }
                        ]}>
                        <Input prefix={<UserOutlined />} placeholder="请输入用户名" type="text" />
                    </Form.Item>
                    <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
                        <Input prefix={<LockOutlined />} placeholder="请输入密码" type="password" />
                    </Form.Item>
                    <Form.Item>
                        <Button htmlType="submit" type="primary" loading={loginLoading}>
                            登录
                        </Button>
                    </Form.Item>
                </Form>
                <div className="company-info">
                    <p className="company-info-tite">© 2024 明略科技 版权所有</p>
                </div>
            </Content>
        </Layout>
    );
};

export default Login;
