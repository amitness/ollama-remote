import subprocess
import shutil
import subprocess
import re

try:
    from rich import print
except ImportError:
    pass


OPENAI_EXAMPLE_CODE = """
# Use below code to access via OpenAI SDK:
-------------------------------------------

from openai import OpenAI

client = OpenAI(
    base_url="{tunnel_url}/v1/",
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
""".strip()

def run_sh(command: str, bg: bool = False):
    kwargs = {"shell": True, "check": True}
    if bg:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    process = subprocess.run(command, **kwargs)
    assert process.returncode == 0


def install_ollama():
    if not shutil.which("ollama"):
        print("Installing Ollama...")
        run_sh("apt install pciutils lshw", bg=True)
        run_sh("curl -fsSL https://ollama.com/install.sh | sh")


def install_cloudflared():
    if not shutil.which("cloudflared"):
        print("Installing Cloudflared...")
        run_sh(
            "wget -q -nc https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo apt install -y -qq ./cloudflared-linux-amd64.deb",
            bg=True,
        )


def serve_ollama():
    subprocess.run("OLLAMA_ORIGINS=* nohup ollama serve &", shell=True)


def expose_ollama_with_cloudflared(port: int = 11434):
    cmd = f'cloudflared tunnel --url http://localhost:{port} --http-host-header="localhost:{port}"'
    try:
        with subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        ) as process:
            for line in process.stdout:
                # Wait for the domain to be assigned
                if ".trycloudflare.com" in line:
                    # Extract the domain
                    domain = re.search(r"https://[^ ]+\.trycloudflare\.com", line)
                    if domain:
                        tunnel_url = domain.group(0)
                        print("Setup is complete.")
                        print("# Commands:")
                        print("---" * 15)
                        ollama_command = f"\nexport OLLAMA_HOST='{tunnel_url}'\n\n"
                        print(ollama_command)
                        print("ollama run phi3:mini --verbose\n\n")
                        print(OPENAI_EXAMPLE_CODE.replace("{tunnel_url}", tunnel_url))
            process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Command '{cmd}' failed with return code {e.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    install_ollama()
    install_cloudflared()
    serve_ollama()
    expose_ollama_with_cloudflared()


if __name__ == "__main__":
    main()
