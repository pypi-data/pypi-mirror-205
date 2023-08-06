import os
import pkg_resources
import sys


def main():
    bin_cmd_sh = pkg_resources.resource_filename(__name__, 'bin/cmd.sh')
    os.system(bin_cmd_sh + " " + " ".join(sys.argv[1:]))


if __name__ == '__main__':
    main()
