"""Canaveral entry point script."""
# canaveral/__main__.py

from canaverall import cli, __app_name__

def main() -> None:
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()