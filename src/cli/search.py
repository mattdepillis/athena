import typer

app = typer.Typer(help="Search memory semantically")

@app.command()
def text():
    typer.secho(f"✓ Searched text files with: ", fg=typer.colors.GREEN)
    # TODO: run semantic search
