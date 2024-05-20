const https = require('https');

const [, , tokens, projectName, message, useName, pipelineLink, env] = process.argv;
const envMap = {
    develop: 'dev环境',
    test: 'test环境',
    master: '生产环境'
};

function formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

async function sendWxMessage(token) {
    const url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + token;
    let className = 'info';

    if (message && (message.indexOf('失败') > -1 || message.indexOf('正在部署') > -1)) {
        className = 'warning';
    }

    const data = JSON.stringify({
        msgtype: 'markdown',
        markdown: {
            content: `<font color=\"${className}\">[${projectName}(By ${useName})]</font>\n<font color=\"${className}\">${
                envMap[env] || env
            }${message}</font>\n[PipelineLink](${pipelineLink})\n<font color=\"comment\">${formatDate(
                new Date()
            )}</font>`
        }
    });

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;'
        }
    };

    try {
        const response = await new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let body = '';

                res.setEncoding('utf8');

                res.on('data', (chunk) => {
                    body += chunk;
                });

                res.on('end', () => {
                    resolve(body);
                });
            });

            req.on('error', (err) => {
                reject(err);
            });

            req.write(data);
            req.end();
        });

        console.log(response);
    } catch (error) {
        console.error(error);
    }
}

tokens.split(',').forEach((token) => {
    if (token) {
        sendWxMessage(token);
    }else{
      console.error('no token received');
    }
});
