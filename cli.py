import click
import subprocess
import tempfile
import os
from src.compiler import compile_tc_to_nasm


@click.group()
def cli():
    """A simple CLI tool for TinyCompiled."""
    pass


def compile_to_nasm(input_file, output_file=None, verbose=False, debug=False, stdout=False):
    """Compile TinyCompiled source to NASM assembly."""
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()

        if verbose:
            click.echo(f"Compiling {input_file}")

        nasm_code = compile_tc_to_nasm(source_code, debug=debug)

        if stdout or output_file is None:
            click.echo(nasm_code)
        else:
            with open(output_file, 'w') as f:
                f.write(nasm_code)
            if verbose:
                click.echo(f"NASM code written to {output_file}")

        if verbose and not stdout:
            click.echo("Compilation to NASM successful")

    except Exception as e:
        click.echo(f"Compilation failed: {e}", err=True)
        raise


def build_executable(input_file, output_file, verbose=False, debug=False):
    """Compile TinyCompiled source to executable."""
    temp_asm = tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False)
    temp_o = tempfile.NamedTemporaryFile(suffix='.o', delete=False)

    try:
        # Compile to NASM
        # Since we need the asm, compile to temp
        nasm_code = compile_tc_to_nasm(open(input_file).read(), debug=debug)
        temp_asm.write(nasm_code)
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
@click.argument("output_file", type=click.Path(), required=False)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--debug", is_flag=True, help="Show debug information including tokens and AST during compilation.")
def compile(input_file, output_file, verbose, debug):
    """Compile TinyCompiled source to NASM assembly.

    Compiles the given TinyCompiled source file to NASM x86-64 assembly code.

    INPUT_FILE: Path to the TinyCompiled source file (.tc)
    OUTPUT_FILE: Path to write the NASM assembly file (.asm). If not provided, outputs to stdout.
    """
    compile_to_nasm(input_file, output_file, verbose, debug)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--debug", is_flag=True, help="Show debug information including tokens and AST during compilation.")
def build(input_file, output_file, verbose, debug):
    """Compile TinyCompiled source to executable.

    Compiles the given TinyCompiled source file to an executable binary.
    Requires NASM and LD to be installed.

    INPUT_FILE: Path to the TinyCompiled source file (.tc)
    OUTPUT_FILE: Path to write the executable file.
    """
    build_executable(input_file, output_file, verbose, debug)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), help="Optional path to save the executable file. If not provided, a temporary executable is used and deleted after running.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--debug", is_flag=True, help="Show debug information including tokens and AST during compilation.")
def run(input_file, output, verbose, debug):
    """Compile and run TinyCompiled source.

    Compiles the given TinyCompiled source file to an executable and runs it.
    Requires NASM and LD to be installed.

    INPUT_FILE: Path to the TinyCompiled source file (.tc)
    """
    if output:
        build_executable(input_file, output, verbose, debug)
        exe_name = output
        if verbose:
            click.echo(f"Running {exe_name}")
        subprocess.run([exe_name], check=True)
    else:
        temp_exe = tempfile.NamedTemporaryFile(suffix='', delete=False)
        temp_exe_name = temp_exe.name
        temp_exe.close()
        try:
            build_executable(input_file, temp_exe_name, verbose, debug)
            if verbose:
                click.echo(f"Running {temp_exe_name}")
            subprocess.run([temp_exe_name], check=True)
        finally:
            os.unlink(temp_exe_name)


if __name__ == "__main__":
    cli()