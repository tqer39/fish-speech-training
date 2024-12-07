import subprocess
import os
import argparse
from argparse import Namespace
from typing import Optional


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(description="protobuf ファイルを生成します。")
    parser.add_argument("--model-name", "-M", type=str, help="モデル名を指定します。")
    parser.add_argument(
        "--force",
        "-F",
        action="store_true",
        help="[OPTION] 既存の protos ファイルがある場合に強制的に上書きします。",
    )
    parser.add_argument(
        "--directory",
        "-D",
        required=True,
        help="[REQUIRED] YYMMDD_HHMMSS フォーマットのディレクトリ名を指定します。",
    )
    return parser.parse_args()

        help="[OPTION] 処理対象のディレクトリを指定します。デフォルトは './data/{model_name}/raw/{directory}/before_text_reformatting' です。",
    )
    return parser.parse_args()


def create_protobuf(input_dir: str, output_dir: str, force: bool) -> None:
    """
    データセットを protobuf ファイルに変換します。
    """
    if force:
        for file in os.listdir(output_dir):
            if file.endswith(".protos"):
                os.remove(os.path.join(output_dir, file))
                print(f"削除されたファイル: {file}")

    os.makedirs(output_dir, exist_ok=True)
    command = [
        ".venv/Scripts/python",
        "tools/llama/build_dataset.py",
        "--input",
        input_dir,
        "--output",
        output_dir,
        "--text-extension",
        ".lab",
        "--num-workers",
        "16",
    ]
    subprocess.run(command, check=True)


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。コマンドライン引数を解析し、protobuf ファイルを生成します。
    """
    if args is None:
        args = parse_arguments()

    model_name = os.getenv("MODEL_NAME") or args.model_name
    if not model_name:
        print("モデル名が指定されていません。")
        return

    directory = os.getenv("FS_DATA_TS") or args.directory

    target_dir = (
        args.override_path
        or f"./data/{model_name}/raw/{directory}/npy"
    )
    output_dir = f"./data/{model_name}/raw/{directory}/protobuf"

    create_protobuf(target_dir, output_dir, args.force)


if __name__ == "__main__":
    main()
