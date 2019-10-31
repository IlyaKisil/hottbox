import click
from hottbox.contrib.visualisation.dash.index import app

@click.command()
@click.option('--host', type=click.Choice(["localhost", "0.0.0.0"], case_sensitive=False), default="localhost")
@click.option('--port', type=click.IntRange(8050, 8060), default="8050")
@click.option('--debug/--no-debug', default=True)
def main(host, port, debug):
    app.run_server(
        host=host,
        port=port,
        debug=debug
    )


if __name__ == '__main__':
    main()
