import os
import argparse
import shutil
from argparse import Namespace
from datetime import datetime

def parse_arguments() -> Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="音声ファイルを指定のディレクトリにコピーします。"
    )
    # [REQUIRED] 引数
    model_name_default = os.getenv("MODEL_NAME")
    parser.add_argument(
        "--model-name", "-M", required=not bool(model_name_default), default=model_name_default, help="[REQUIRED] コピー先のディレクトリ名"
    )

    # [OPTION] 引数
    parser.add_argument(
        "--directory", "-D",
        help="[OPTION] 元になる音声ファイル（mp3, wav など）のパスを指定するディレクトリ",
    )
    parser.add_argument(
        "--force", "-F",
        action="store_true",
        help="[OPTION] 同名のファイルがある場合に強制的に上書きします。",
    )
    return parser.parse_args()

def main(args=None):
    """
    メイン関数。音声ファイルを指定のディレクトリにコピーします。
    """
    if args is None:
        args = parse_arguments()

    if args.directory:
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        raw_dir = os.path.join(f"./data/{args.model_name}", "raw", timestamp)
        os.makedirs(raw_dir, exist_ok=True)
        for file in os.listdir(args.directory):
            if file.endswith((".mp3", ".wav")):
                dest_file = os.path.join(raw_dir, file)
                if os.path.exists(dest_file) and not args.force:
                    print(f"スキップされたファイル: {dest_file}（既に存在します）")
                else:
                    shutil.copy(
                        os.path.join(args.directory, file), dest_file
                    )
                    print(f"コピーされたファイル: {dest_file}")

if __name__ == "__main__":
    main()
