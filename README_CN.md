<div align="center">

# Open Assistant API

_✨ 开箱即用的 AI 智能助手 API ✨_

</div>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_CN.md">简体中文</a> |
  <a href="./README_JP.md">日本語</a>
</p>

## 简介

Open Assistant API 是一个开源自托管的 AI 智能助手 API，兼容 OpenAI 官方接口，
可以直接使用 OpenAI 官方的 [Client](https://github.com/openai/openai-python) 构建 LLM 应用。

支持 [One API](https://github.com/songquanpeng/one-api) 可以用其接入更多商业和私有模型。

支持 [R2R](https://github.com/SciPhi-AI/R2R) RAG 引擎。

## 使用

以下是使用了 OpenAI 官方的 Python `openai` 库的使用示例:

```python
import openai

client = openai.OpenAI(
    base_url="http://127.0.0.1:8086/api/v1",
    api_key="xxx"
)

assistant = client.beta.assistants.create(
    name="demo",
    instructions="You are a helpful assistant.",
    model="gpt-4-1106-preview"
)
```

## 为什么选择 Open Assistant API

| 功能               | Open Assistant API | OpenAI Assistant API |
|------------------|--------------------|----------------------|
| 生态策略             | 开源                 | 闭源                   |
| RAG 引擎           | 支持 R2R             | 支持                   |
| 联网搜索             | 支持                 | 不支持                  |
| 自定义 Functions    | 支持                 | 支持                   |
| 内置 Tool          | 支持扩展               | 不支持扩展                |
| Code Interpreter | 待开发                | 支持                   |
| 多模态识别            | 支持                 | 支持                   |
| LLM 支持           | 支持更多的 LLM          | 仅 GPT                |
| Message 流式输出     | 支持                 | 支持                   |
| 本地部署             | 支持                 | 不支持                  |

- **LLM 支持**: 相较于 OpenAI 官方版本，可以通过接入 One API 来支持更多的模型。
- **Tool**: 目前支持联网搜索；可以较容易扩展更多的 Tool。
- **RAG 引擎**: 支持 R2R RAG 引擎，目前支持的文件类型有 txt、html、markdown、pdf、docx、pptx、xlsx、png、mp3、mp4 等。
- **Message 流式输出**: 支持 Message 流式输出，提供更流畅的用户体验。
- **生态策略**: 开源，你可以将服务部署在本地，可以对已有功能进行扩展。

## 快速上手

启动 Open Assistant API 最简单方法是运行 docker-compose.yml 文件。 运行之前确保机器上安装了 Docker 和 Docker Compose。

### 配置

进入项目根目录，打开 `docker-compose.yml`，填写 openai api_key 和 bing search key (非必填)。

```sh
# openai api_key (支持 OneAPI api_key)
OPENAI_API_KEY=<openai_api_key>

# bing search key (非必填)
BING_SUBSCRIPTION_KEY=<bing_subscription_key>
````

建议配置 R2R RAG 引擎替换默认的 RAG 实现，以提供更好的 RAG 能力。
关于 R2R，可以通过 [R2R Github 仓库](https://github.com/SciPhi-AI/R2R) 了解和使用。

```sh
# RAG 配置
# FILE_SERVICE_MODULE=app.services.file.impl.oss_file.OSSFileService
FILE_SERVICE_MODULE=app.services.file.impl.r2r_file.R2RFileService
R2R_BASE_URL=http://<r2r_api_address>
R2R_USERNAME=<r2r_username>
R2R_PASSWORD=<r2r_password>
```

### 运行

#### 使用 Docker Compose 运行:

 ```sh
docker compose up -d
 ```

### 访问 API

Api Base URL: http://127.0.0.1:8086/api/v1

接口文档地址: http://127.0.0.1:8086/docs

### 完整使用示例

此示例中使用 OpenAI 官方的 client 库创建并运行了一个 AI 助手。如果需要查看其它使用方式，如流式输出、工具（web_search、retrieval、function)的使用等，
可以在 examples 查看对应示例。
运行之前需要运行 `pip install openai` 安装 Python `openai` 库。

```sh
# !pip install openai
export PYTHONPATH=$(pwd)
python examples/run_assistant.py
```

### 权限
基于 token 提供简单用户隔离，满足 SaaS 部署需求，可通过配置 ```APP_AUTH_ENABLE``` 开启

![](docs/imgs/user.png)

1. 验证方式为 Bearer token，可在 Header 中填入 ```Authorization: Bearer ***``` 进行验证
2. token 管理参考 api 文档中的 token 小节
相关 api 需通过 admin token 验证，配置为 ```APP_AUTH_ADMIN_TOKEN```，默认为 admin
3. 创建 token 需填入大模型 base_url 和 api_key，创建的 assistant 将使用相关配置访问大模型
### 工具
根据 OpenAPI /Swagger规范，允许将多种工具集成到助手中，赋予并增强了LLM 连接外部世界的能力。

1. 方便将你的应用与其他系统或服务连接，与外部环境交互，如代码执行、对专属信息源的访问
2. 在使用过程中，需创建工具，接着将工具与助手搭配即可，查看测试用例[Assistant With Action](tests/tools/assistant_action_test.py)
2. 若需要使用带认证信息的工具，只需在运行时添加认证信息即可，具体参数格式可在接口文档中查看。查看测试用例[Run With Auth Action](tests/tools/run_with_auth_action_test.py)

## 社区与支持

- 加入 [Slack](https://join.slack.com/t/openassistant-qbu7007/shared_invite/zt-29t8j9y12-9og5KZL6GagXTEvbEDf6UQ)
  频道，查看新发布的内容，交流问题，参与社区互动。
- 加入 [Discord](https://discord.gg/VfBruz4B) 频道，与其他社区成员交流。
- 加入 Open Assistant Api 微信交流群：

  ![](docs/imgs/wx.png)

## 特别感谢

我们主要参考和依赖了以下项目:

- [OpenOpenAI](https://github.com/transitive-bullshit/OpenOpenAI): Node 实现的 Assistant API
- [One API](https://github.com/songquanpeng/one-api): 多模型管理工具
- [R2R](https://github.com/SciPhi-AI/R2R): RAG 引擎
- [OpenAI-Python](https://github.com/openai/openai-python): OpenAI Python Client
- [OpenAI API](https://github.com/openai/openai-openapi): OpenAI 接口定义
- [LangChain](https://github.com/langchain-ai/langchain): LLM 应用开发库
- [OpenGPTs](https://github.com/langchain-ai/opengpts): LangChain GPTs
- [TaskingAI](https://github.com/TaskingAI/TaskingAI): TaskingAI 原生应用开发


## 参与贡献

请阅读我们的[贡献文档](./docs/CONTRIBUTING_CN.md)，了解如何参与贡献。

## 开源协议

本仓库遵循 MIT 开源协议。有关详细信息，请参阅 [LICENSE](./LICENSE) 文件。
