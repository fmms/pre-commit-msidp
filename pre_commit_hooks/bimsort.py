import argparse, sys
import json

def bim_is_unsorted(filename):
    return True

def sbim_sort(filename):
    with open(filename, mode="rb") as file_processed:
        data = json.dumps(json.load(file_processed), sort_keys=True, indent=2, separators=(',', ': '))
    with open(filename, mode="w") as outfile:
        outfile.write(data)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)
    unsorted_bims = [f for f in args.filenames if f.endswith('.bim') and bim_is_unsorted(f)]
    for unsorted_bim in unsorted_bims:
        print(f"Sort .bim file: {unsorted_bim}")
        sbim_sort(unsorted_bim)
    if unsorted_bims:
        print("")
        print(".bim files have been sorted. Now aborting the commit.")
        print(
            'You can check the changes made. Then simply "git add --update ." and re-commit'
        )
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
