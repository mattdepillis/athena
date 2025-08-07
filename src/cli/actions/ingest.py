import typer

from integrations.spotify import ingest as spotify_ingest

app = typer.Typer(help="Ingest data from external sources")


@app.command("spotify")
def ingest_spotify():
    """Ingest Spotify data into Athena."""
    spotify_ingest.run()
