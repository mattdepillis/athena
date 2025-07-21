from pathlib import Path
from typing import Optional

import typer
from rich import print as rp

app = typer.Typer(
    help="Ingest notes or files into Athena memory", invoke_without_command=True
)


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.secho("Error: missing subcommand", fg=typer.colors.RED, err=True)
        rp(
            "Try one of:\n  🔤 [bold magenta]athena ingest text[/bold magenta] ...\n  📁 [bold magenta]athena ingest file[/bold magenta] ...\n  📥 [bold magenta]athena ingest stdin[/bold magenta] ...",
        )
        rp("For all options, try [bold cyan]athena ingest --help[/bold cyan]")
        raise typer.Exit(1)


@app.command()
def text(note: str, tag: str = typer.Option(None, "--tag")):
    """Ingest a raw text note"""
    typer.secho(f"✓ Ingested text: {note}", fg=typer.colors.GREEN)


@app.command()
def file(path: Path, tag: str = typer.Option(None, "--tag")):
    """Ingest from a local file"""
    content = path.read_text()
    typer.secho(f"✓ Ingested file: {content[:100]}", fg=typer.colors.GREEN)


@app.command()
def stdin(tag: str = typer.Option(None, "--tag")):
    """Ingest from standard input"""
    import sys

    content = sys.stdin.read()
    typer.secho(f"✓ Ingested from stdin: {content[:100]}", fg=typer.colors.GREEN)
