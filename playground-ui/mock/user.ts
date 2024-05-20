import { Request, Response } from 'express';
import Mock from 'mockjs';

const waitTime = (time: number = 100) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(true);
        }, time);
    });
};

export default {
    'POST /api/user/login': async (req: Request, res: Response) => {
        await waitTime(100);
        res.cookie('token', 'stone');
        res.json(
            Mock.mock({
                code: 200,
                msg: '请求成功',
                data: {
                    userName: 'test user',
                    userId: 'xxx'
                }
            })
        );
    },
    'POST /api/user/logout': async (req: Request, res: Response) => {
        await waitTime(1000);
        res.json(
            Mock.mock({
                code: 200,
                msg: '注销成功',
                data: {}
            })
        );
    },
    'GET /api/user/userInfo': async (req: Request, res: Response) => {
        await waitTime(1000);
        res.json(
            Mock.mock({
                code: 200,
                msg: '请求成功',
                data: {
                    userName: 'test user',
                    userId: 'xxx'
                }
            })
        );
    }
};
