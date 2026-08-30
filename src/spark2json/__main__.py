import sys

from . import convert


def main():
    if len(sys.argv) < 2:
        print("Usage: spark2json <input.sparkprofile> [output.json|-]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    result = convert(src, dst)
    if dst == '-':
        sys.stdout.write(result)
    else:
        print("Wrote:", result)


if __name__ == '__main__':
    main()
