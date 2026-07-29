import requests
from dotenv import load_dotenv

os = __import__("os")
load_dotenv()


invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False
API_KEY = os.environ.get("NVIDIA_BEARER")
# print(API_KEY)

headers = {
    "Authorization": "Bearer " + API_KEY,
    "Accept": "text/event-stream" if stream else "application/json",
}

payload = {
  "messages": [
    {
      "role": "user",
      "content": "what is the model version? What is training cut off?"
    }
  ],
  "model": "google/diffusiongemma-26b-a4b-it",
  "chat_template_kwargs": {
    "enable_thinking": True
  },
  "max_tokens": 4096,
  "stream": stream,
  "temperature": 1,
  "top_p": 0.95
}

response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)
if stream:
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    print(response.json()["choices"][0]["message"]["reasoning"])