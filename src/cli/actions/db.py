import typer

from db.lib.crud import show_tables_in_db
from db.ops.cleanup import nuke_db, wipe_tables
from db.ops.init import init_db

app = typer.Typer(help="Database ops")

##########################################################################################
################################### OPS-LEVEL FUNCTIONS ##################################
##########################################################################################


@app.command("init")
def cmd_init():
    if typer.confirm("Run all schemas (db/schemas/*.sql)?", default=True):
        init_db()
        typer.echo("✅ DB initialized.")


@app.command("wipe")
def cmd_wipe(internal: bool = typer.Option(False, help="Also wipe internal tables")):
    if typer.confirm("Delete all rows but keep schema?", default=False):
        wipe_tables()
        if internal and typer.confirm(
            "Also wipe internal tracking tables?", default=False
        ):
            # optional: implement a wipe_internal() call in cleanup.py
            pass
        typer.echo("🧹 Wiped data.")


@app.command("nuke")
def cmd_nuke():
    if typer.confirm("Permanently delete athena.db?", default=False):
        nuke_db()
        typer.echo("💣 DB deleted.")


##########################################################################################
################################### LIB-LEVEL FUNCTIONS ##################################
##########################################################################################


@app.command("show-tables")
def show_tables():
    """Show all tables in the DB."""
    # from config import DB_PATH  # or wherever your db path lives
    from pathlib import Path

    DB_PATH = Path("athena.db")

    tables = show_tables_in_db(DB_PATH)
    typer.echo("\n".join(tables))
