<div align="center">

# Open Assistant API

_✨ An out-of-the-box AI intelligent assistant API ✨_

</div>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_CN.md">简体中文</a> |
  <a href="./README_JP.md">日本語</a>
</p>

## Introduction

Open Assistant API is an open-source, self-hosted AI intelligent assistant API that’s compatible with the official OpenAI
interface. It can be seamlessly used with the official OpenAI [Client](https://github.com/openai/openai-python) to create
LLM applications.

It also supports [One API](https://github.com/songquanpeng/one-api) for integration with a broader range of commercial and private models.

Additionally, it includes integration with the [R2R](https://github.com/SciPhi-AI/R2R) RAG engine.

## Usage

Below is an example of using the official OpenAI Python `openai` library:

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



Why Choose Open Assistant API
Feature	Open Assistant API	OpenAI Assistant API
Ecosystem Strategy	Open Source	Closed Source
RAG Engine	Supports R2R	Supported
Internet Search	Supported	Not Supported
Custom Functions	Supported	Supported
Built-in Tools	Extendable	Not Extendable
Code Interpreter	In Development	Supported
Multimodal	Supported	Supported
LLM Support	More LLMs	Only GPT
Message Streaming Output	Supported	Supported
Local Deployment	Supported	Not Supported


LLM Support: Compatible with a wider range of models via One API integration.
Toolset: Currently supports online search and can be expanded with additional tools.
RAG Engine: Supports file types like txt, html, markdown, pdf, docx, pptx, xlsx, png, mp3, mp4, and more.
Message Streaming: Provides smoother message streaming for enhanced user interaction.
Open Source: Completely open-source for local deployment and customization.



Quick Start
The easiest way to launch the Open Assistant API is by using the Docker Compose file. Ensure Docker and Docker Compose are installed on your system.

Configuration
Navigate to the project root, open docker-compose.yml, and fill in your OpenAI API key and Bing search key (optional).

sh
Copy code
# openai api_key (supports OneAPI api_key)
OPENAI_API_KEY=<openai_api_key>

# bing search key (optional)
BING_SUBSCRIPTION_KEY=<bing_subscription_key>
Configuring the R2R RAG engine is recommended for a better RAG experience. You can set this up through the R2R repository.

sh
# RAG config
# FILE_SERVICE_MODULE=app.services.file.impl.oss_file.OSSFileService
FILE_SERVICE_MODULE=app.services.file.impl.r2r_file.R2RFileService
R2R_BASE_URL=http://<r2r_api_address>
R2R_USERNAME=<r2r_username>
R2R_PASSWORD=<r2r_password>


Run
Run with Docker Compose:
sh
Copy code
docker compose up -d
Access API
API Base URL: http://127.0.0.1:8086/api/v1
Documentation: http://127.0.0.1:8086/docs
Complete Usage Example
Below is a basic example to create and run an AI assistant using the OpenAI client. For other advanced features like streaming output, online tools, or custom functions, check the examples directory. Before starting, install the OpenAI Python library:

sh
Copy code
# !pip install openai
export PYTHONPATH=$(pwd)
python examples/run_assistant.py
Permissions
User isolation is implemented based on tokens for SaaS deployment support. To enable, configure APP_AUTH_ENABLE.



Use Bearer token for authentication. Include Authorization: Bearer *** in the header.
Token management details can be found in the API documentation under the token section. Admin token, set as APP_AUTH_ADMIN_TOKEN, defaults to "admin".
When creating a token, specify the base URL and API key. The assistant will use these settings to access the model.
Tools
Following OpenAPI/Swagger standards, the assistant can integrate various tools to enhance external connectivity.

Enables integration with other systems or services for tasks like code execution or data access.
Tools need to be created before they can be used with the assistant. See test cases for more details: Assistant With Action.
For tools requiring authentication, add auth details at runtime. Detailed parameter formats are in the API documentation. More details are in the test cases: Run With Auth Action.
Community and Support
Join our Slack channel for discussions, updates, and support.

Connect with community members on Discord.

Join our WeChat group:



Special Thanks
This project builds on the following incredible open-source projects:

OpenOpenAI: Node-based Assistant API
One API: Multi-model management
R2R: RAG engine
OpenAI-Python: OpenAI Python client
OpenAI API: OpenAI API interface definition
LangChain: LLM application development library
OpenGPTs: LangChain GPTs
TaskingAI: TaskingAI client SDK
Contributing
Please refer to our Contribution Guide to learn how to get involved and contribute.

