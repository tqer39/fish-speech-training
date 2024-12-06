import argparse
import os
import subprocess

def parse_arguments():
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(description="音声データから npy ファイルを生成します。")
    parser.add_argument('--directory', '-D', type=str, required=True, help='入力音声ファイルが含まれるディレクトリのパス')
    parser.add_argument('--checkpoint-path', type=str, help='チェックポイントファイルのパス (環境変数 FS_CHECKPOINT_PATH が優先されます)')
    return parser.parse_args()

def generate_npy(input_file: str, checkpoint_path: str):
    """
    npy ファイルを生成します。
    """
    output_file = os.path.splitext(input_file)[0] + '.npy'
    command = [
        'python', 'tools/vqgan/inference.py',
        '-i', input_file,
        '--checkpoint-path', checkpoint_path,
        '-o', output_file
    ]
    subprocess.run(command, check=True)

def main():
    args = parse_arguments()

    directory = args.directory
    checkpoint_path = os.getenv('FS_CHECKPOINT_PATH') or args.checkpoint_path

    if not checkpoint_path:
        print("チェックポイントファイルのパスが指定されていません。")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.wav', '.mp3')):
                input_file = os.path.join(root, file)
                generate_npy(input_file, checkpoint_path)

if __name__ == "__main__":
    main()
