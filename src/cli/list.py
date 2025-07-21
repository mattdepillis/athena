import typer
from typing import Optional

app = typer.Typer(help="List resources indexed by Athena")

@app.command()
def all():
    """
    List ingested resources, optionally filtered by tag or count.
    """
    print("[cyan]Listing resources:[/cyan]")
    typer.secho(f"✓ Listed resources: ", fg=typer.colors.GREEN)
