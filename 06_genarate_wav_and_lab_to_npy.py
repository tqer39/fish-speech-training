import subprocess
import os
import argparse
from argparse import Namespace
from typing import Optional


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="wav と lab ファイルを npy ファイルに変換します。"
    )
    parser.add_argument("--model-name", "-M", type=str, help="モデル名を指定します。")
    parser.add_argument(
        "--directory",
        "-D",
        type=str,
        help="[REQUIRED] YYMMDD_HHMMSS フォーマットのディレクトリ名を指定します。",
    )
    parser.add_argument(
        "--checkpoint-path",
        type=str,
        default="checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth",
        help="チェックポイントファイルのパスを指定します。",
    )
    parser.add_argument(
        "--config-name",
        type=str,
        default="firefly_gan_vq",
        help="設定ファイルの名前を指定します。",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=1,
        help="ワーカーの数を指定します。",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="バッチサイズを指定します。",
    )
    return parser.parse_args()


def run_extract_vq(target_dir: str, args: Namespace) -> None:
    """
    extract_vq.py スクリプトを実行します。
    """
    command = [
        ".venv/Scripts/python",
        "tools/vqgan/extract_vq.py",
        target_dir,
        "--num-workers",
        str(args.num_workers),
        "--batch-size",
        str(args.batch_size),
        "--config-name",
        args.config_name,
        "--checkpoint-path",
        args.checkpoint_path,
    ]
    subprocess.run(command, check=True)


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。extract_vq.py スクリプトを実行します。
    """
    if args is None:
        args = parse_arguments()

    model_name = os.getenv("MODEL_NAME") or args.model_name
    if not model_name:
        print("モデル名が指定されていません。")
        return

    directory = os.getenv("FS_DATA_TS") or args.directory
    if not directory:
        print("ディレクトリが指定されていません。")
        return

    target_dir = f"./data/{model_name}/raw/{directory}/dataset"

    run_extract_vq(target_dir, args)


if __name__ == "__main__":
    main()
