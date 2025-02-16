# Ollama Remote

Expose and get a URL for ollama on any remote server.

## Usage
Install the package via `pip`.

```bash
pip install ollama-remote
```

Then, just run `ollama-remote` on the remote server and it will give you back the URL.

```zsh
ollama-remote
```

You will get back the commands to copy and run locally.

<p align="center">
<img width="791" alt="image" src="https://github.com/user-attachments/assets/c163fe38-6b93-4c76-aa15-5e730e1f2237" />
</p>

## Usecase 1: Run via ollama

For example, if you were assigned this url, running it locally will allow you to pull and run any ollama model. You need to have `ollama` installed locally.

```bash
export OLLAMA_HOST='https://spa-visiting-voices-omissions.trycloudflare.com'
ollama run phi3:mini --verbose
```

The model is actually downloaded and run on the server-side, so if the server has GPUs, it will be faster.

<p align="center">
<img width="653" alt="image" src="https://github.com/user-attachments/assets/18b74fc6-50df-4958-850f-aa028fed743b" />
</p>

The commands are same as regular ollama. 
```
ollama pull phi3:mini
ollama run phi3:mini
```

## Usecase 2: OpenAI SDK
You are also provided code to use the model through the OpenAI SDK. 

If you wanted to use `phi3:mini`, you have to make sure to have run `ollama pull phi3:mini` before this.

Then the code is same as above:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://spa-visiting-voices-omissions.trycloudflare.com/v1/",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="phi3:mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)
print(response.choices[0].message.content)
```

<img width="1008" alt="image" src="https://github.com/user-attachments/assets/d1884687-9f7f-4763-8d7a-237fad8a6abb" />

