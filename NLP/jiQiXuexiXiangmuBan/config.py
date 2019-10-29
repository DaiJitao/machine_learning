import argparse

def get_args():
    parser = argparse.ArgumentParser()

    # data
    parser.add_argument("--train-file", type=str, default=None, help="")
    print(parser.parse_args())
    return parser.parse_args()


