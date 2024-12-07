# fish-speech-training

fish-speech を動かすためのスクリプトを管理するリポジトリ。
PowerShell を管理者権限で実行することを前提とする。

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
huggingface-cli download fishaudio/fish-speech-$env:FS_VERSION --local-dir $env:FS_CHECKPOINT

# やり直し用
# uv rm --python "$PYTHON_VERSION" torch torchvision torchaudio
```

## スクリプトをシムリンク

このプロジェクトのルートにある python スクリプトを fish-speech のディレクトリにシムリンクする。

```powershell
# まずスクリプトのファイルをリストに入れる
$scripts = @(
    "01_file_copy.py",
    "02_separate.py",
    "03_normalize.py",
    "04_generate_wav_to_npy.py",
    "05_speech_to_text.py",
    "06_generate_wav_and_lab_to_npy.py",
    "07_create_protobuf.py"
)

# fish-speech のディレクトリにシムリンクを作成する
foreach ($script in $scripts) {
    $dest = Join-Path -Path $env:WORKSPACE -ChildPath "fish-speech\$script"
    New-Item -ItemType SymbolicLink -Path $dest -Value $script -Force
}
```

### 一括でシムリンクを解除する場合

```powershell
foreach ($script in $scripts) {
    $dest = Join-Path -Path $env:WORKSPACE -ChildPath "fish-speech\$script"
    Remove-Item -Path $dest
}
```

### 個別でシムリンクを解除する場合

```powershell
Remove-Item Join-Path -Path $env:WORKSPACE -ChildPath "fish-speech\01_file_copy.py"
```

## ファイルコピー

```powershell
cd $env:WORKSPACE\fish-speech
.venv\Scripts\python 01_file_copy.py -D .\data\source\sample
```

## ファイルの分割

`-D` オプションには、ファイルコピーで生成されたディレクトリ名を指定する。

```powershell
$env:FS_DATA_TS = "YYMMDD_HMMMSS"
.venv\Scripts\python 02_separate.py
```

## ファイルの正規化

```powershell
.venv\Scripts\python 03_normalize.py
```

## 音声データから npy ファイルを生成

これは正直やらなくてもいいかもしれない。

```powershell
.venv\Scripts\python 04_generate_wav_to_npy.py
```

## 音声データから文字起こしファイルを生成

```powershell
.venv\Scripts\python 05_speech_to_text.py
```

## npy ファイルと lab ファイルを元に npy ファイルを生成

```powershell
.venv\Scripts\python 06_generate_wav_and_lab_to_npy.py
```

## Protobuf ファイルの生成

```powershell
.venv\Scripts\python 07_create_protobuf.py
```
