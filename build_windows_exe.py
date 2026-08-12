import os
import subprocess
import sys
from pathlib import Path


def build_exe():
    base_dir = Path(__file__).resolve().parent
    launcher = base_dir / 'launcher.py'

    if not launcher.exists():
        raise FileNotFoundError('launcher.py not found. Create launcher.py in the project root.')

    data_paths = [
        (base_dir / 'templates', 'templates'),
        (base_dir / 'inventory' / 'static', os.path.join('inventory', 'static')),
    ]

    add_data_args = []
    pathsep = ';' if os.name == 'nt' else ':'
    for source, target in data_paths:
        if source.exists():
            add_data_args.extend(['--add-data', f'{source}{pathsep}{target}'])

    args = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--clean',
        '--name',
        'warehouse_management',
        '--console',
        '--hidden-import',
        'webview',
        *add_data_args,
        str(launcher),
    ]

    print('Building Windows executable for Django app...')
    print('Command:', ' '.join(args))
    subprocess.run(args, check=True)
    print('\nBuild finished successfully.')
    print('Find the executable in the dist folder: dist\\warehouse_management.exe')


if __name__ == '__main__':
    build_exe()
