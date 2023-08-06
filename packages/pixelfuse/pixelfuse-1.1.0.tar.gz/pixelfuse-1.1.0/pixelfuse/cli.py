import typer
from typing import Optional
from rich import print

from pixelfuse.src.f2v import ToVideo
from pixelfuse.src.v2f import ToFile
from pixelfuse.src.old_files.d_v1 import ToFile as dv1ToFile

app = typer.Typer()

@app.command(name="videoToFile")
def convertToFile(path: str, verbose: Optional[int]=2, decoder: Optional[str]=""):
    try:
        match decoder:
            case "":
                c = ToFile(path, verbose)
                c.convert()
            case "v1":
                c = dv1ToFile(path, verbose)
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
    path: str,
    fps: Optional[float]=1.,
    width: Optional[int]=640,
    height: Optional[int]=480,
    fourcc: Optional[str]="HFYU",
    output: Optional[str]="output.avi",
    verbose: Optional[int]=2,
):
    try:
        c = ToVideo(path, fps, width, height, fourcc, output, verbose)
        c.convert()
    except FileNotFoundError:
        print(f"[red bold]File {path} doesn't exist")
    except Exception as e:
        print("[red bold]Unknown error:")
        print(e)