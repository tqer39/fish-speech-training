# fish-speech-training

## 環境変数

事前に環境変数を設定しておく。

```powershell
$env:WORKSPACE = "ワークスペースパス"
$env:FS_REPO_URL = "fish-speech のリポジトリ URL"
$env:FS_VERSION = "fish-speech のバージョン"
$env:FS_CHECKPOINT = "fish-speech のチェックポイント"
$env:FS_CHECKPOINT_PATH = "fish-speech のチェックポイントのパス"
$env:MODEL_NAME = "モデル名"
```

## fish-speech を動かすまで

```powershell
# powershell で実行する
git clone $env:FS_REPO_URL $env:WORKSPACE\fish-speech
cd $env:WORKSPACE\fish-speech

# local
$PYTHON_VERSION="3.10.0"
uv python pin $PYTHON_VERSION
uv venv --python "$PYTHON_VERSION"

# activate
. ".\.venv\Scripts\activate.ps1"
python -V # Python 3.10.0
python -m ensurepip --default-pip
uv pip install --upgrade pip
uv pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
uv pip install fish-audio-preprocess pydub whisper click
uv pip install -e .[stable]
pip install huggingface-hub
huggingface-cli download fishaudio/fish-speech-$env:FS_VERSION --local-dir checkpoints/fish-speech-$env:FS_VERSION

# やり直し用
# uv rm --dev --python "$PYTHON_VERSION" torch torchvision torchaudio
```

## ファイルコピー

```powershell
$env:MODEL_NAME = "fish-speech-1.4"
```
