#!python
# -*- mode: python ; coding: utf-8 -*-

import click
import os
from urllib.request import urlopen

__version__ = "0.17.0"

@click.group()
def cli():
    pass

@click.command(name='install')
@click.argument('package')
def install(package):
        
    if package:

        with urlopen(f"https://raw.githubusercontent.com/AquaQuokka/pygmi-pkgs/main/packages/{package}/{package}.py") as u:
            pkgu = str(u.read())

        if pkgu != "404: Not Found":
        
            if not os.path.exists(f"pygmi"):
                os.mkdir(f"pygmi")

            if not os.path.exists(os.path.join(f"pygmi", f"{package}.py")):
                with open(os.path.join(f"pygmi", f"{package}.py"), 'w') as f:
                    f.write(str(pkgu))
                    click.echo(f"\033[33;1mPackage {package} installed successfully.\033[0m")

            else:
                click.echo(f"\033[33;1m{package}.py already exists, are you sure you want to update it?\033[0m")
                cfm = input(f"Update {package}.py? (Y/n): ")
                
                if cfm.strip().lower() in ["y", "yes"]:
                    with open(os.path.join(f"pygmi", f"{package}.py"), 'w') as f:
                        f.write('')
                        f.write(str(pkgu))
                        click.echo(f"\033[33;1mPackage {package} updated successfully.\033[0m")
                
                else:
                    click.echo(f"\033[31mSkipped package.\033[0m")


    
        else:
            click.echo(f"\033[0;31mPackage {package} not found!\033[0m")
    
    else:
        click.echo(f"\033[0;31mFatal: Expected 1 argument: package\033[0m")

cli.add_command(install)

def main():
    cli()

if __name__ == "__main__":
    main()