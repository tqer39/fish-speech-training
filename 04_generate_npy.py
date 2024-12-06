import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Generate npy files from audio data")
    parser.add_argument('--input', '-I', type=str, required=True, help='Path to the input audio file (wav, mp3)')
    parser.add_argument('--checkpoint-path', type=str, required=True, help='Path to the checkpoint file')
    args = parser.parse_args()

    input_file = args.input
    checkpoint_path = args.checkpoint_path

    os.system(f'python tools/vqgan/inference.py -i "{input_file}" --checkpoint-path "{checkpoint_path}"')

if __name__ == "__main__":
    main()
