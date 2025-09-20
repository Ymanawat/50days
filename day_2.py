from litellm import completion
import os
import json
from dotenv import load_dotenv
load_dotenv()

messages=[
    {
        "content": "add 10 and 20",
        "role": "user"
    }
]

response = completion(model="openai/gpt-4o", messages=messages)

# print complete response
print(json.dumps(response.model_dump(), indent=4))
print("---------------------")


# print only llm text response
print('llm text reponse:')
print(response.choices[0].message.content)