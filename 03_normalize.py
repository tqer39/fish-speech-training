import sys
import argparse
import subprocess
import os
from argparse import Namespace
from typing import Optional


def parse_arguments() -> argparse.ArgumentParser:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="音声ファイルにラウドネス正規化を適用します。"
    )
    parser.add_argument("--directory", "-D", help="[OPTION] 入力ディレクトリのパス")
    parser.add_argument("--model-name", "-M", help="[OPTION] モデル名を指定します。")
    parser.add_argument(
        "--loudness-target",
        type=float,
        default=-23.0,
        help="[OPTION] ラウドネス正規化のターゲット値（dB LUFS）。デフォルトは -23.0 dB LUFS です。"
        "ターゲット値を上げると音量が大きくなり、下げると音量が小さくなります。",
    )
    parser.add_argument(
        "--force",
        "-F",
        action="store_true",
        help="[OPTION] ラウドネス正規化を強制します。",
    )
    return parser


def normalize_loudness(input_dir: str, output_dir: str, loudness_target: float) -> None:
    """
    ディレクトリ内の音声ファイルにラウドネス正規化を適用します。
    """
    command = [
        "fap",
        "loudness-norm",
        input_dir,
        output_dir,
        "--clean",
        "--loudness",
        str(loudness_target),
    ]
    subprocess.run(command, check=True)


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。コマンドライン引数を解析し、音声ファイルのコピーと分割を実行します。
    """
    parser = parse_arguments()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    model_name = os.getenv("MODEL_NAME") or args.model_name
    if not model_name:
        print("モデル名が指定されていません。")
        sys.exit(1)

    directory = os.getenv("FS_DATA_TS") or args.directory
    if not directory:
        print(
            "エラー: --directory オプションまたは FS_DATA_TS 環境変数を指定してください。"
        )
        sys.exit(1)

    input_dir = f"./data/{model_name}/raw/{directory}/separate"
    normalize_dir = f"./data/{model_name}/raw/{directory}/normalize_loudness"
    os.makedirs(normalize_dir, exist_ok=True)
    normalize_flag_file = os.path.join(normalize_dir, ".normalized")

    # ラウドネス正規化を適用
    if os.path.exists(normalize_flag_file) and not args.force:
        print("ラウドネス正規化は既に適用されています。")
    else:
        normalize_loudness(input_dir, normalize_dir, args.loudness_target)
        with open(normalize_flag_file, "w") as f:
            f.write("normalized")
        print("ラウドネス正規化を適用しました。")


if __name__ == "__main__":
    main()
