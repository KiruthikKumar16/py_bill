import os
import sys
import threading

from django.core.management import execute_from_command_line

try:
    import webview
except ImportError:
    webview = None


def start_server(host: str, port: str):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warehouse.settings')
    execute_from_command_line([sys.argv[0], 'runserver', '--noreload', f'{host}:{port}'])


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    host = '127.0.0.1'
    port = '8000'
    url = f'http://{host}:{port}/'

    server_thread = threading.Thread(target=start_server, args=(host, port), daemon=True)
    server_thread.start()

    if webview:
        webview.create_window('Warehouse Pro', url, width=1200, height=820)
    else:
        print('pywebview is not installed. Install pywebview to launch the app in a native window.')
        print('Falling back to the system browser instead.')
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
        server_thread.join()


if __name__ == '__main__':
    main()
