import os
import argparse
from argparse import Namespace
from typing import Optional
import whisper


def parse_arguments() -> Namespace:
    """
    コマンドライン引数を解析します。
    """
    parser = argparse.ArgumentParser(
        description="音声ファイルからテキストデータを抽出し、同名のファイルに保存します。"
    )
    parser.add_argument(
        "--input-dir", required=True, help="[REQUIRED] 入力音声ファイルのディレクトリ"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="[REQUIRED] 出力テキストファイルのディレクトリ",
    )
    parser.add_argument(
        "--extension",
        type=str,
        default="lab",
        help="[OPTION] 出力ファイルの拡張子。デフォルトは 'lab' です。",
    )
    parser.add_argument(
        "--whisper-model",
        "-W",
        help="[OPTION] Whisper モデル名（環境変数 WHISPER_MODEL からも読み取ります）",
    )
    return parser.parse_args()


def speech_to_text(input_file: str, model_name: str) -> str:
    """
    音声ファイルからテキストデータを抽出します。
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(input_file, language="ja")
    return result["text"]


def main(args: Optional[Namespace] = None) -> None:
    """
    メイン関数。音声ファイルからテキストデータを抽出し、同名のファイルに保存します。
    """
    if args is None:
        args = parse_arguments()

    whisper_model = args.whisper_model or os.getenv("WHISPER_MODEL")
    if not whisper_model:
        print(
            "Whisper モデル名が指定されていません。--whisper-model オプションまたは WHISPER_MODEL 環境変数を設定してください。"
        )
        return

    os.makedirs(args.output_dir, exist_ok=True)

    for file in sorted(os.listdir(args.input_dir)):
        if file.endswith((".mp3", ".wav")):
            input_file: str = os.path.join(args.input_dir, file)
            output_file: str = os.path.join(
                args.output_dir, os.path.splitext(file)[0] + f".{args.extension}"
            )
            text: str = speech_to_text(input_file, whisper_model)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"テキストデータを保存しました: {output_file}")
            print(f"テキストの内容: {text}")


if __name__ == "__main__":
    main()
