import jinja2
from rich import print
import typer

def create_oam_file(oam_file_data: dict):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader('canaveral/templates/'))
    template = environment.get_template('vela_template.yaml')
    with open("vela.yaml", "w") as f:
        f.write(template.render(oam_file_data))
        f.close()
    print("The file is most likely [bold red]incomplete[/bold red], please check it and fill the missing fields by consulting the OAM specification")
    typer.confirm(text="Confirm [Enter]", default=True, show_default=False)
    