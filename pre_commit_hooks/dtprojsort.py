import argparse, sys
from lxml import etree
import pickle

def dtproj_is_unsorted(filename):
    root = etree.parse(filename).getroot()
    ns = { 'SSIS' : "www.microsoft.com/SqlServer/SSIS" }
    # packages
    listOfPackageNames_before=root.xpath('//SSIS:Project/SSIS:Packages/SSIS:Package/@SSIS:Name', namespaces=ns)
    packages=root.xpath('//SSIS:Project/SSIS:Packages', namespaces=ns)[0]
    packages[:] = sorted(packages, key=lambda child: child.xpath('.//@SSIS:Name', namespaces=ns)[0])
    listOfPackageNames_after=root.xpath('//SSIS:Project/SSIS:Packages/SSIS:Package/@SSIS:Name', namespaces=ns)

    # package_meta_data
    listOfPackageMetadata_before=root.xpath('//SSIS:Project/SSIS:DeploymentInfo/SSIS:PackageInfo/SSIS:PackageMetaData/@SSIS:Name', namespaces=ns)
    package_meta_data=root.xpath('//SSIS:Project/SSIS:DeploymentInfo/SSIS:PackageInfo', namespaces=ns)[0]
    package_meta_data[:] = sorted(package_meta_data, key=lambda child: child.xpath('.//@SSIS:Name', namespaces=ns)[0])
    listOfPackageMetadata_after=root.xpath('//SSIS:Project/SSIS:DeploymentInfo/SSIS:PackageInfo/SSIS:PackageMetaData/@SSIS:Name', namespaces=ns)
    return not(listOfPackageNames_after == listOfPackageNames_before and listOfPackageMetadata_after == listOfPackageMetadata_before)

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

def dtproj_sort(filename):
    # https://stackoverflow.com/questions/72114455/xml-sorting-with-python
    # https://stackoverflow.com/questions/46566216/writing-lxml-etree-with-double-quotes-header-attributes
    root = etree.parse(filename).getroot()
    ns = { 'SSIS' : "www.microsoft.com/SqlServer/SSIS" }
    packages=root.xpath('//SSIS:Project/SSIS:Packages', namespaces=ns)[0]
    packages[:] = sorted(packages, key=lambda child: child.xpath('.//@SSIS:Name', namespaces=ns)[0])
    package_meta_data=root.xpath('//SSIS:Project/SSIS:DeploymentInfo/SSIS:PackageInfo', namespaces=ns)[0]
    package_meta_data[:] = sorted(package_meta_data, key=lambda child: child.xpath('.//@SSIS:Name', namespaces=ns)[0])

    with open(filename, 'wb') as f:
        f.write(etree.tostring(root, doctype='<?xml version="1.0" encoding="utf-8"?>', encoding='utf-8', pretty_print = False))

    # unfortunately lxml does not retain whitespace, thus adding it again to not clutter diffs
    fix_unintended_lxml_file_modifications(filename)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)
    unsorted_dtprojs = [f for f in args.filenames if f.endswith('.dtproj') and dtproj_is_unsorted(f)]
    for unsorted_dtproj in unsorted_dtprojs:
        print(f"Sort .dtproj file: {unsorted_dtproj}")
        dtproj_sort(unsorted_dtproj)
    if unsorted_dtprojs:
        print("")
        print(".dtproj files have been sorted. Now aborting the commit.")
        print(
            'You can check the changes made. Then simply "git add --update ." and re-commit'
        )
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
