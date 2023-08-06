import os
import sys

def main():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(package_dir, '..', 'bin')
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    script_path = os.path.join(bin_dir, 'test_push_swap.py')
    with open(script_path, 'w') as f:
        f.write('#!/usr/bin/env python\n')
        f.write('from test_push_swap import test_push_swap\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    test_push_swap.main()\n')
    os.chmod(script_path, 0o755)
    print('Added {} to PATH.'.format(script_path))

if __name__ == '__main__':
    main()

