import typer

from db.spin import cleanup, init

app = typer.Typer(help="Database management")


@app.command("init")
def init_db():
    cleanup = typer.confirm(
        "This will run all schema migrations. Continue?",
        default=True,  # default if only enter is pressed
    )
    if cleanup:
        init.init_db()
        print("🧼 DB initialized.")


@app.command("wipe")
def wipe():
    confirm = typer.confirm(
        "This will delete all records but keep the schema. Continue?"
    )
    if confirm:
        cleanup.wipe_tables()
        print("🧼 All tables wiped.")
    else:
        print("Record deletion unconfirmed. Skipping for now...")


@app.command("nuke")
def nuke():
    confirm = typer.confirm(
        "This will permanently delete the entire DB file. Continue?"
    )
    if confirm:
        cleanup.delete_db_file()
        print("🧼 DB file deleted.")
    else:
        print("DB file deletion unconfirmed. Skipping for now...")
