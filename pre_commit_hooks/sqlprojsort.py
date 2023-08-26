import argparse, sys
from lxml import etree
import pickle

def sqlproj_is_unsorted(filename):
    root = etree.parse(filename).getroot()
    ns = { 'x' : "http://schemas.microsoft.com/developer/msbuild/2003" }
    # folders
    listOfFolderIncludes_before=root.xpath('/x:Project/x:ItemGroup/x:Folder/@Include', namespaces=ns)
    folders=root.xpath('/x:Project/x:ItemGroup/x:Folder', namespaces=ns)[0].getparent()
    folders[:] = sorted(folders, key=lambda child: child.xpath('.//@Include', namespaces=ns)[0])
    listOfFolderIncludes_after=root.xpath('/x:Project/x:ItemGroup/x:Folder/@Include', namespaces=ns)

    # builds
    listOfBuildIncludes_before=root.xpath('/x:Project/x:ItemGroup/x:Build/@Include', namespaces=ns)
    builds=root.xpath('/x:Project/x:ItemGroup/x:Build', namespaces=ns)[0].getparent()
    builds[:] = sorted(builds, key=lambda child: child.xpath('.//@Include', namespaces=ns)[0])
    listOfBuildIncludes_after=root.xpath('/x:Project/x:ItemGroup/x:Build/@Include', namespaces=ns)

    return not(listOfFolderIncludes_after == listOfFolderIncludes_before and listOfBuildIncludes_after == listOfBuildIncludes_before)

def fix_unintended_lxml_file_modifications(filename):
    LF = b'\n'
    CRLF = b'\r\n'
    with open(filename, mode="rb") as file_processed:
        lines = file_processed.readlines()
    lines = [line.replace(b"/>", b" />") for line in lines]
    lines = [line.replace(LF, CRLF) for line in lines]
    with open(filename, mode="wb") as file_processed:
        for line in lines:
            file_processed.write(line)

def sqlproj_sort(filename):
    # https://stackoverflow.com/questions/72114455/xml-sorting-with-python
    # https://stackoverflow.com/questions/46566216/writing-lxml-etree-with-double-quotes-header-attributes
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(filename, parser).getroot()
    ns = { 'x' : "http://schemas.microsoft.com/developer/msbuild/2003" }
    folders=root.xpath('/x:Project/x:ItemGroup/x:Folder', namespaces=ns)[0].getparent()
    folders[:] = sorted(folders, key=lambda child: child.xpath('.//@Include', namespaces=ns)[0])
    builds=root.xpath('/x:Project/x:ItemGroup/x:Build', namespaces=ns)[0].getparent()
    builds[:] = sorted(builds, key=lambda child: child.xpath('.//@Include', namespaces=ns)[0])

    with open(filename, 'wb') as f:
        f.write(etree.tostring(root, doctype='<?xml version="1.0" encoding="utf-8"?>', encoding='utf-8', pretty_print = True))

    # unfortunately lxml does not retain whitespace, thus adding it again to not clutter diffs
    fix_unintended_lxml_file_modifications(filename)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)
    unsorted_sqlprojs = [f for f in args.filenames if f.endswith('.sqlproj') and sqlproj_is_unsorted(f)]
    for unsorted_sqlproj in unsorted_sqlprojs:
        print(f"Sort .sqlproj file: {unsorted_sqlproj}")
        sqlproj_sort(unsorted_sqlproj)
    if unsorted_sqlprojs:
        print("")
        print(".sqlproj files have been sorted. Now aborting the commit.")
        print(
            'You can check the changes made. Then simply "git add --update ." and re-commit'
        )
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
