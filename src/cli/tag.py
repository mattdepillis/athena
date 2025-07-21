import typer

app = typer.Typer(help="Manage tags for notes")

@app.command(name="tag")
def tag_resource(tag: str, to: str):
    typer.secho(f"✓ Tagged resource {to} with: {tag}", fg=typer.colors.GREEN)
