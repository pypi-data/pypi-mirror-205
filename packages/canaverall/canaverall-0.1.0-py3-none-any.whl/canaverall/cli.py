"""This module provides the Canaveral CLI"""
# canaveral/cli.py

from typing import Optional
from pathlib import Path
import typer
import shutil
import yaml
from canaverall import __app_name__, __version__
from canaverall.merge_oam import merge_oam
from canaverall.create_oam import create_oam_file
from canaverall.oam_form import oam_form

app = typer.Typer()

def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def create():
    """Interactively Create a OAM file"""
    oam_form_data = oam_form()
    create_oam_file(oam_form_data)


@app.command()
def default():
    """Create the default OAM file"""
    shutil.copyfile("canaveral/templates/vela_default.yaml", "vela.yaml")
    

@app.command()
def merge(dev: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
          ops: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True)):
    """Merge Dev OAM file with Operations OAM file"""
    dev_yaml = yaml.load(dev.open(), Loader=yaml.FullLoader)
    ops_yaml = yaml.load(ops.open(), Loader=yaml.FullLoader)

    merged = merge_oam(dev_yaml, ops_yaml)
    
    with open("vela.yaml", "w") as f:
        yaml.dump(merged, f)
        f.close()
    # INFO: Library hiyapyco doesn't work as expected, it doesn't merge nested lists
    # conf = hiyapyco.load([dev.absolute().as_posix(), ops.absolute().as_posix()], method=hiyapyco.METHOD_MERGE, interpolate=True)
    # print(type(conf))
    # with open("vela.yaml", "w") as f:
    #     f.write(hiyapyco.dump(conf, default_flow_style=False))
    #     f.close()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

