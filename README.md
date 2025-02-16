# ollama-remote

Automatically configure and obtain a URL for Ollama on any remote Linux server (GPU Providers, Google Colab, Kaggle, etc.) using the Cloudflared tunnel..

> Note: For Google Colab, here is an example [notebook](https://colab.research.google.com/drive/1pmSzR8mGAUOtu8SHfD75XowncodRyygo?usp=sharing). This is only allowed if you are a paid colab user as per their [terms of service](https://research.google.com/colaboratory/faq.html#disallowed-activities). If you use it for free account, do it at your own risk.

This is useful for faster experimentation if the ollama model run too slow locally, and for synthetic data generation in large batches.

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
Once you set `OLLAMA_HOST` to the assigned URL, you can run any ollama commands on your local terminal. It will feel like working locally, but the actual model inference happens on the server side. Make sure you have `ollama` CLI installed locally.

```bash
export OLLAMA_HOST='https://spa-visiting-voices-omissions.trycloudflare.com'
ollama run phi3:mini --verbose
```

If the server has GPUs such as Colab, this will be much faster.

<p align="center">
<img width="653" alt="image" src="https://github.com/user-attachments/assets/18b74fc6-50df-4958-850f-aa028fed743b" />
</p>

The commands are same as regular ollama and you can download any models that fits on the GPU server-side. 
```
ollama pull phi3:mini
ollama run phi3:mini
```

## Usecase 2: OpenAI SDK
You are also provided code to use the model through the OpenAI SDK. Make sure to pull the model specified in the code beforehand via `ollama pull phi3:mini`.

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

