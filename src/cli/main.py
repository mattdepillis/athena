import typer

from cli import ingest, list, search, tag

app = typer.Typer(help="Athena CLI - developer-first semantic memory")

# Add subcommands
app.add_typer(ingest.app, name="ingest")
app.add_typer(list.app, name="list")
app.add_typer(search.app, name="search")
app.add_typer(tag.app, name="tag")
