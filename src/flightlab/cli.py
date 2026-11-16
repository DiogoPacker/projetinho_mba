import argparse
import json

from flightlab.data import download, load
from flightlab.model import train


def main():
    parser = argparse.ArgumentParser(description="FlightLab — pipeline de dados e treinamento")
    parser.add_argument("command", choices=["download", "train", "quality"])
    args = parser.parse_args()
    if args.command == "download":
        print(f"Dataset salvo em {download()}")
        return
    df, quality = load()
    result = train(df, quality) if args.command == "train" else quality
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
