import typer

from cli.actions import db, feedback, ingest, suggest

app = typer.Typer(help="Athena CLI — developer-first semantic memory")

app.add_typer(db.app, name="db")
app.add_typer(ingest.app, name="ingest")
