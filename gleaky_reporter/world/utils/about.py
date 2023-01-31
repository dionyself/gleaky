import sys
from os.path import join
import pkg_resources


def get_licenses():

    licenses = {}

    # loading requirements.txt data (if present)
    requirements_path = join(sys.path[0], "requirements.txt")
    requirements = []
    try:
        with open(requirements_path, 'r') as f:
            requirements = f.readlines()
    except:
        print("requirements.txt not found (%s)" % requirements_path)

    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        name = str(pkg)
        lic = "(Licence not found)"
        try:
            lines = pkg.get_metadata_lines('METADATA')
        except:
            lines = pkg.get_metadata_lines('PKG-INFO')

        for line in lines:
            if line.startswith('License:'):
                lic = line[9:]

        # checking requirements.txt data (if present)
        if requirements:
            ignore_pkg = True
            for req in requirements:
                if name.split()[0] in req:
                    ignore_pkg = False
            if ignore_pkg:
                continue

        licenses[name] = lic
    return licenses
