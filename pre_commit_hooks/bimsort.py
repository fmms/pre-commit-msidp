import argparse, sys
import json

def tabular_editor_sort(e):
    return e.casefold().replace("-", "")

def sort_bim_json (jsonObject):
    changed = False
    if "model" in jsonObject.keys():
        print ("has a model...")
        if "dataSources" in jsonObject["model"]:
            print ("sorting datasources")
            before = [ds["name"] for ds in jsonObject["model"]["dataSources"]]
            jsonObject["model"]["dataSources"] = sorted(jsonObject["model"]["dataSources"], key = lambda e: tabular_editor_sort(e["name"]))
            after = [ds["name"] for ds in jsonObject["model"]["dataSources"]]
            if (before != after):
                print("changed from", before, "to", after, ".")
                changed = True
        if "tables" in jsonObject["model"]:
            print ("sorting tables")
            before = [ds["name"] for ds in jsonObject["model"]["tables"]]
            jsonObject["model"]["tables"] = sorted(jsonObject["model"]["tables"], key = lambda e: tabular_editor_sort(e["name"]))
            after = [ds["name"] for ds in jsonObject["model"]["tables"]]
            if (before != after):
                print("changed from", before, "to", after, ".")
                changed = True
            for t in jsonObject["model"]["tables"]:
                 if "columns" in t.keys():
                    print ("sorting columns of", t["name"])
                    before = [ds["name"] for ds in t["columns"]]
                    t["columns"]= sorted(t["columns"], key = lambda e: tabular_editor_sort(e["name"]) + ".json")
                    after = [ds["name"] for ds in t["columns"]]
                    if (before != after):
                        print("changed from", before, "to", after, ".")
                        changed = True
        if "relationships" in jsonObject["model"]:
            print ("sorting relationships")
            before = [ds["name"] for ds in jsonObject["model"]["relationships"]]
            jsonObject["model"]["relationships"] = sorted(jsonObject["model"]["relationships"], key = lambda e: tabular_editor_sort(e["name"]))
            after = [ds["name"] for ds in jsonObject["model"]["relationships"]]
            if (before != after):
                print("changed from", before, "to", after, ".")
                changed = True
        if "roles" in jsonObject["model"]:
            print ("sorting roles")
            before = [ds["name"] for ds in jsonObject["model"]["roles"]]
            jsonObject["model"]["roles"] = sorted(jsonObject["model"]["roles"], key = lambda e: tabular_editor_sort(e["name"]))
            after = [ds["name"] for ds in jsonObject["model"]["roles"]]
            if (before != after):
                print("changed from", before, "to", after, ".")
                changed = True
    return changed, jsonObject

def bim_is_unsorted(filename):
    with open(filename, mode="rb") as file_processed: 
        jsonObject = json.load(file_processed)
        isSorted, trash = sort_bim_json(jsonObject)
    return isSorted

def bim_sort(filename):
    with open(filename, mode="rb") as file_processed:
        jsonObject = json.load(file_processed)
        trash, jsonObject = sort_bim_json(jsonObject)
        data = json.dumps(jsonObject, sort_keys=False, indent=2, separators=(',', ': '), ensure_ascii=False)
    with open(filename, mode="w", encoding='utf8') as outfile:
        outfile.write(data)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)
    unsorted_bims = [f for f in args.filenames if f.endswith('.bim') and bim_is_unsorted(f)]
    for unsorted_bim in unsorted_bims:
        print(f"Sort .bim file: {unsorted_bim}")
        bim_sort(unsorted_bim)
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
