import glob
import hashlib
import os
from pathlib import Path
import tarfile
from typing import Optional

import typer
from rich import print
from rich.console import Console

from pixelfuse.src.f2v import ToVideo
from pixelfuse.src.v2f import ToFile

app = typer.Typer()

@app.command(name="filesToVideo")
def filesToVideo(
    paths: list[Path]=typer.Argument(..., help="PathS to be converted to video. It can be either a file path or a folder path"),
    fps: Optional[float]=typer.Option(1., help="Frame rate of video"),
    width: Optional[int]=typer.Option(640, help="Video length"),
    height: Optional[int]=typer.Option(480, help="Video height"),
    fourcc: Optional[str]=typer.Option("HFYU", help="Codec, a string of 4 characters, WARNING: Use lossless codecs ONLY"),
    output: Optional[Path]=typer.Option("output.avi", help="Path to output file, note you need to use file extension compatible with codec, for example if you use HFYU codec you can NOT specify output as output.mp4"),
    verbose: Optional[int]=typer.Option(2, help="Output level from 0 to 3")
):
    console = Console()

    with console.status("[green]Creating archive...", spinner="dots12"):
        archive = tarfile.open(output.with_suffix(".tar.gz"), 'w:gz')
        hashmap = {}

        for path in paths:
            if not path.exists():
                continue
            try:
                if path.is_file():
                    archive.add(path)
                    hashmap[path] = hashlib.sha512(path.read_bytes()).hexdigest()
                    console.print(f"[green]Added to archive:[/green] [magenta italic]{path}[/magenta italic] | {hashmap[path][:7]}")
                    continue

                for file in path.rglob("**/*"):
                    if file.is_file() and output.with_suffix(".tar.gz").name not in file.name:
                        archive.add(file)
                        hashmap[file] = hashlib.sha512(file.read_bytes()).hexdigest()
                        console.print(f"[green]Added to archive:[/green] [magenta italic]{file}[/magenta italic] | {hashmap[file][:7]}")
            except FileNotFoundError:
                continue

        archive.close()

    try:
        c = ToVideo(output.with_suffix(".tar.gz"), fps, width, height, fourcc, output, verbose, hashmap)
        c.convert()
        output.with_suffix(".tar.gz").unlink()
    except FileNotFoundError:
        print(f"[red bold]File {path} doesn't exist")
    except Exception as e:
        print("[red bold]Unknown error:")
        print(e)

@app.command(name="videoToFile")
def convertToFile(
    path: Path=typer.Argument(..., help="The path to the video you want to convert back to a file"),
    verbose: Optional[int]=typer.Option(2, help="Output level, from 0 to 2"),
    exctractDir: Optional[str]=typer.Option(None, help="Path to extract archive files"),
):
    try:
        c = ToFile(path, verbose, exctractDir)
        c.convert()
    except FileExistsError as e:
        print(f"[red bold]{e}")
    except UnicodeDecodeError as e:
        print(f"[red bold]Cannot decode frames:[/red bold] {e}")
    except Exception as e:
        print(f"[red bold]Unknown error:")
        print(e)

@app.command(name="fileToVideo")
def convertToVideo(
    path: Path=typer.Argument(..., help="The path to the file you want to convert"),
    fps: Optional[float]=typer.Option(1., help="Frame rate of video"),
    width: Optional[int]=typer.Option(640, help="Video length"),
    height: Optional[int]=typer.Option(480, help="Video height"),
    fourcc: Optional[str]=typer.Option("HFYU", help="Codec, a string of 4 characters, WARNING: Use lossless codecs ONLY"),
    output: Optional[Path]=typer.Option("output.avi", help="Path to output file, note you need to use file extension compatible with codec, for example if you use HFYU codec you can NOT specify output as output.mp4"),
    verbose: Optional[int]=typer.Option(2, help="Output level from 0 to 3"),
):
    try:
        c = ToVideo(path, fps, width, height, fourcc, output, verbose)
        c.convert()
    except FileNotFoundError:
        print(f"[red bold]File {path} doesn't exist")
    except Exception as e:
        print("[red bold]Unknown error:")
        print(e)