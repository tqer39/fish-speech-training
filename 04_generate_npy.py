import argparse
import os
import subprocess

def parse_arguments():
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(description="音声データから npy ファイルを生成します。")
    parser.add_argument('--directory', '-D', type=str, required=True, help='入力音声ファイルが含まれるディレクトリのパス')
    parser.add_argument('--model-name', '-M', help='モデル名（環境変数 MODEL_NAME からも読み取ります）')
    parser.add_argument('--checkpoint-path', type=str, help='チェックポイントファイルのパス (環境変数 FS_CHECKPOINT_PATH が優先されます)')
    return parser.parse_args()

def generate_npy(input_file: str, output_dir: str, checkpoint_path: str):
    """
    npy ファイルを生成します。
    """
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.npy')
    command = [
        '.venv\\Scripts\\python', 'tools/vqgan/inference.py',
        '-i', input_file,
        '--checkpoint-path', checkpoint_path,
        '-o', output_file
    ]
    print(f"Executing command: {' '.join(command)}")  # デバッグ用にコマンドを出力
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode('utf-8', errors='ignore')}")
    else:
        print(f"Generated npy file: {output_file}")

def main():
    args = parse_arguments()

    directory = args.directory
    model_name = os.getenv("MODEL_NAME") or args.model_name
    checkpoint_path = os.getenv('FS_CHECKPOINT_PATH') or args.checkpoint_path

    if not model_name:
        print("モデル名が指定されていません。")
        return

    if not checkpoint_path:
        print("チェックポイントファイルのパスが指定されていません。")
        return

    input_dir = f"./data/{model_name}/raw/{directory}/normalize_loudness"
    output_dir = os.path.join(f"./data/{model_name}/raw/{directory}/npy")
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.wav', '.mp3')):
                input_file = os.path.join(root, file)
                generate_npy(input_file, output_dir, checkpoint_path)

if __name__ == "__main__":
    main()
