import subprocess

def main():
    """
    メイン関数。extract_vq.py スクリプトを実行します。
    """
    command = [
        "python",
        "tools/vqgan/extract_vq.py",
        "data",
        "--num-workers", "1",
        "--batch-size", "16",
        "--config-name", "firefly_gan_vq",
        "--checkpoint-path", "checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
