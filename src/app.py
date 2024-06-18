import argparse

from server import run_server
from services import Hamster, Bloom


def main():
    parser = argparse.ArgumentParser(description="Run various services")
    parser.add_argument('--server', action='store_true', help="Run the server")
    parser.add_argument('--hamster-kombat', action='store_true', help="Run HamsterKombat")
    parser.add_argument('--bloom', action='store_true', help="Run Bloom")

    args = parser.parse_args()

    if args.server:
        run_server()
    elif args.hamster_kombat:
        Hamster().run()
    elif args.bloom:
        Bloom().run()
    else:
        print("No valid arguments provided. Use --server, --hamster-kombat, or --bloom")


if __name__ == '__main__':
    main()
