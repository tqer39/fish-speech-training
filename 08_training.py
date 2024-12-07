import subprocess
import os
from typing import Optional
import sys
import argparse
from argparse import Namespace


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="Fine-tuning script for GenLipSyncVideo"
    )
    parser.add_argument(
        "--model-name", "-M", type=str, help="Name of the model to fine-tune"
    )
    parser.add_argument(
        "--directory",
        "-D",
        type=str,
        help="[REQUIRED] YYMMDD_HHMMSS フォーマットのディレクトリ名を指定します。",
    )
    parser.add_argument(
        "--config-name", "-C", type=str, required=True, help="Config name for training"
    )
    return parser.parse_args()


def training(project: str, config_name: str) -> None:
    """
    モデルをトレーニングします。
    """
    os.environ["HYDRA_FULL_ERROR"] = "1"  # エラー詳細を表示する

    command = [
        ".venv/Scripts/python",
        "fish_speech/train.py",
        "--config-name",
        config_name,
        f"project={project}",
        "+lora@model.model.lora_config=r_8_alpha_16",
    ]
    subprocess.run(command, check=True)


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。コマンドライン引数を解析し、fine tuning の処理を実行します。
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

    training(model_name, args.config_name)


if __name__ == "__main__":
    main()
