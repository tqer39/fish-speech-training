# fish-speech-training

## fish-speech を動かすまで

```powershell
git clone https://github.com/fishaudio/fish-speech
cd ./fish-speech
uv python pin 3.13.0

pip install huggingface-hub
huggingface-cli download fishaudio/fish-speech-1.4 --local-dir checkpoints/fish-speech-1.4

$PYTHON_VERSION="3.10.0"
uv venv --python "$PYTHON_VERSION"

. ".\.venv\Scripts\activate.ps1"
python -V # Python 3.10.0
python -m ensurepip --default-pip
uv pip install --upgrade pip

uv pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
uv pip install fish-audio-preprocess pydub whisper click
uv pip install -e .[stable]

# やり直し用
# uv rm --dev --python "$PYTHON_VERSION" torch torchvision torchaudio
```

## 環境変数

`MODEL_NAME` という環境変数にモデル名を設定する。

```powershell
$env:WORKSPACE = "ワークスペースパス"
$env:FS_REPO_URL = "fish-speech のリポジトリ URL"
$env:FS_CHECKPOINT = "fish-speech のチェックポイント"
$env:FS_CHECKPOINT_PATH = "fish-speech のチェックポイントのパス"
$env:MODEL_NAME = "モデル名"
```
