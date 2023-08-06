import os
from importlib import resources
import sys


def main():
    bin_cmd_sh = resources.path('py3dpolys_le.bin', 'cmd.sh')
    os.system(bin_cmd_sh + " " + " ".join(sys.argv[1:]))


if __name__ == '__main__':
    main()
