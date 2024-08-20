import logging
import openai

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Use this client to run examples. 
# If you have enabled authentication management, please set the 'api_key'. Otherwise, you can ignore this parameter.
base_url = "http://localhost:8086/api/v1"
api_key = "ml-xxx"
client = openai.OpenAI(base_url=base_url, api_key=api_key)
