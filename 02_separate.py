import os
import argparse
import subprocess
from argparse import Namespace
from typing import Optional
from datetime import timedelta


def parse_arguments() -> Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="音声ファイルを指定の間隔で分割します。"
    )
    parser.add_argument(
        "--directory", "-D", required=True, help="[REQUIRED] 入力ディレクトリのパス"
    )
    parser.add_argument(
        "--model-name",
        "-M",
        help="[OPTION] モデル名（環境変数 MODEL_NAME からも読み取ります）",
    )
    parser.add_argument(
        "--start", type=int, default=0, help="[OPTION] 分割開始時間（秒）"
    )
    parser.add_argument(
        "--interval", type=int, default=30, help="[OPTION] 分割間隔（秒）"
    )
    parser.add_argument(
        "--overlay", type=int, default=5, help="[OPTION] 分割の重なり（秒）"
    )
    parser.add_argument(
        "--force",
        "-F",
        action="store_true",
        help="[OPTION] 既存ファイルを強制的に上書きします。",
    )
    parser.add_argument("--output-dir", help="[OPTION] 出力ディレクトリのパス")
    return parser.parse_args()


def format_time(seconds: int) -> str:
    """
    秒数を hh:mm:ss の形式にフォーマットします。
    """
    td = timedelta(seconds=seconds)
    return str(td).zfill(8)  # ゼロサプライして hh:mm:ss の形式にする


def generate_output_filename(
    base_filename: str,
    segment_number: int,
    start_time: int,
    end_time: int,
    file_extension: str,
) -> str:
    """
    分割後のファイル名を生成します。
    """
    start_time_str: str = format_time(start_time).replace(":", "-")
    end_time_str: str = format_time(end_time).replace(":", "-")
    return f"{base_filename}_{segment_number:05d}_{start_time_str}~{end_time_str}{file_extension}"


def get_audio_duration(input_file: str) -> int:
    """
    音声ファイルの総再生時間を取得します。
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_file,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return int(float(result.stdout))


def split_audio_file(
    input_file: str,
    output_dir: str,
    start_time: int,
    interval: int,
    overlay: int,
    force: bool,
) -> None:
    """
    音声ファイルを指定の間隔で分割し、出力ディレクトリに保存します。
    """
    duration: int = interval
    total_duration: int = get_audio_duration(input_file)

    # 出力ディレクトリの存在確認
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 入力ファイルの存在確認
    if not os.path.isfile(input_file):
        print(f"入力ファイルが見つかりません: {input_file}")
        return

    segment_number: int = 1
    current_time: int = start_time

    while current_time < total_duration:
        base_filename: str = os.path.splitext(os.path.basename(input_file))[0]
        file_extension: str = os.path.splitext(input_file)[1]
        output_filename: str = generate_output_filename(
            base_filename,
            segment_number,
            current_time,
            min(current_time + duration, total_duration),
            file_extension,
        )
        output_filepath: str = os.path.join(output_dir, output_filename)

        if os.path.exists(output_filepath):
            if force:
                os.remove(output_filepath)
            else:
                print(f"スキップされたファイル: {output_filepath}（既に存在します）")
                segment_number += 1
                current_time += interval - overlay
                continue

        command: list[str] = [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            str(current_time),
            "-t",
            str(min(duration, total_duration - current_time)),
            "-c",
            "copy",
            output_filepath,
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            break
        print(f"出力ファイル: {output_filepath}")
        segment_number += 1
        current_time += interval - overlay


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。コマンドライン引数を解析し、音声ファイルを分割します。
    """
    if args is None:
        args = parse_arguments()

    model_name = args.model_name or os.getenv("MODEL_NAME")
    if not model_name:
        print(
            "モデル名が指定されていません。--model-name オプションまたは MODEL_NAME 環境変数を設定してください。"
        )
        return

    input_dir = f"./data/{model_name}/raw/{args.directory}"
    output_dir = args.output_dir or os.path.join(input_dir, "separate")

    if not os.path.isdir(input_dir):
        print(f"入力ディレクトリが見つかりません: {input_dir}")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            input_file = os.path.join(root, file)
            split_audio_file(
                input_file,
                output_dir,
                args.start,
                args.interval,
                args.overlay,
                args.force,
            )


if __name__ == "__main__":
    main()
