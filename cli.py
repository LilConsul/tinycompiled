import click
from src.compiler import compile_tc_to_nasm


@click.group()
def cli():
    """A simple CLI tool."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def compile(input_file, output_file):
    with open(input_file, "r") as f:
        source_code = f.read()

    nasm_code = compile_tc_to_nasm(source_code)

    with open(output_file, "w") as f:
        f.write(nasm_code)


cli.add_command(compile)


if __name__ == "__main__":
    cli()