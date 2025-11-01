import click
import subprocess
import tempfile
import os
from src.compiler import compile_tc_to_nasm


@click.group()
def cli():
    """A simple CLI tool for TinyCompiled."""
    pass


def compile_to_nasm(input_file, output_file, verbose=False):
    """Compile TinyCompiled source to NASM assembly."""
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()

        if verbose:
            click.echo(f"Compiling {input_file} to {output_file}")

        nasm_code = compile_tc_to_nasm(source_code)

        with open(output_file, 'w') as f:
            f.write(nasm_code)

        if verbose:
            click.echo("Compilation to NASM successful")

    except Exception as e:
        click.echo(f"Compilation failed: {e}", err=True)
        raise


def build_executable(input_file, output_file, verbose=False):
    """Compile TinyCompiled source to executable."""
    temp_asm = tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False)
    temp_o = tempfile.NamedTemporaryFile(suffix='.o', delete=False)

    try:
        # Compile to NASM
        compile_to_nasm(input_file, temp_asm.name, verbose)
        temp_asm.close()

        # Assemble
        if verbose:
            click.echo(f"Assembling {temp_asm.name} to {temp_o.name}")
        subprocess.run(['nasm', '-f', 'elf64', '-o', temp_o.name, temp_asm.name], check=True)

        # Link
        if verbose:
            click.echo(f"Linking {temp_o.name} to {output_file}")
        subprocess.run(['ld', temp_o.name, '-o', output_file], check=True)

        if verbose:
            click.echo("Build successful")

    except subprocess.CalledProcessError as e:
        click.echo(f"Build failed during assembly/linking: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"Build failed: {e}", err=True)
        raise
    finally:
        if os.path.exists(temp_asm.name):
            os.unlink(temp_asm.name)
        if os.path.exists(temp_o.name):
            os.unlink(temp_o.name)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def compile(input_file, output_file, verbose):
    """Compile TinyCompiled source to NASM assembly."""
    compile_to_nasm(input_file, output_file, verbose)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def build(input_file, output_file, verbose):
    """Compile TinyCompiled source to executable."""
    build_executable(input_file, output_file, verbose)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def run(input_file, verbose):
    """Compile and run TinyCompiled source."""
    temp_exe = tempfile.NamedTemporaryFile(suffix='', delete=False)
    temp_exe_name = temp_exe.name
    temp_exe.close()  # Close the file handle so build_executable can write to it
    try:
        build_executable(input_file, temp_exe_name, verbose)
        if verbose:
            click.echo(f"Running {temp_exe_name}")
        subprocess.run([temp_exe_name], check=True)
    finally:
        os.unlink(temp_exe_name)


if __name__ == "__main__":
    cli()