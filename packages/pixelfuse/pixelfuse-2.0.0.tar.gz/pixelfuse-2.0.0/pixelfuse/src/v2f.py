import hashlib
import os
from pathlib import Path
import pickle
import tarfile
import tempfile

import cv2
import numpy as np
from rich.console import Console

from pixelfuse import compatible_encoders, decoder


class ToFile:
    def __init__(self, filename: Path, verbose, exctractDir):
        self.cap = cv2.VideoCapture(filename.name)
        self.console = Console()
        self.verbose = verbose
        self.exctractDir = exctractDir

        if not self.cap.isOpened(): 
            raise FileNotFoundError("Error opening video file")

    def writeTempFile(self):
        self.print("Start reading video", 1)
        ret, frame = self.cap.read()
        toWriteFrame = None
        self.meta = None
        self.temp = tempfile.NamedTemporaryFile(mode="wb", delete=False, dir="./")
        self.print(f"Created temp file {self.temp.name}", 2)

        while(ret):
            if all(frame[0, 0] == [128, 4, 149]):
                self.print("Found [128  4 149] meta frame", 1)
                self.meta = pickle.loads(bytes(frame.flatten()))

                if self.meta["encoder"] not in compatible_encoders:
                    self.print_verbose(f"[yellow bold]Endcoder {self.meta['encoder']} isn't compatible with {decoder}", 0)

            if toWriteFrame is not None and self.meta is not None:
                self.print(f"Preprocessing last {toWriteFrame[0, 0]} frame...", 1)

                toWriteFrame = toWriteFrame.flatten().reshape((-1, 3))
                while np.all(toWriteFrame[-1] == 0):
                    toWriteFrame = toWriteFrame[:-1]
                toWriteFrame = toWriteFrame.flatten()
                toWriteFrame = toWriteFrame[:len(toWriteFrame)-self.meta["lastZeros"]]

                self.temp.write(toWriteFrame)
                break

            if toWriteFrame is not None:
                self.temp.write(toWriteFrame)

            self.print(f"[green]Done [/green]{frame[0, 0]} [green]frame[/green]", 2)
            
            toWriteFrame = frame
            ret, frame = self.cap.read()

        self.temp.close()
        self.print("[green bold]Done writing temp file", 1)

    def renameAccordingToMeta(self):
        if self.meta["hashmap"] is not None:
            return

        try:
            self.print(f"Rename temp file: {self.temp.name} -> ./{self.meta['filename']}", 1)
            os.link(self.temp.name, self.meta["filename"])
        except FileExistsError:
            os.remove(self.temp.name)
            raise FileExistsError(f"Cannot write file, file already exists: {self.meta['filename']}")

        self.print(f"Remove temp file {self.temp.name}", 2)
        os.remove(self.temp.name)

    def extract(self):
        if self.meta["hashmap"] is not None:
            self.print(f"Extracting files...", 2)
            archive = tarfile.open(self.temp.name, "r:gz")
            if self.exctractDir is None:
                self.exctractDir = self.meta["filename"].split(".")[0]
            archive.extractall(self.exctractDir)
            archive.close()

            self.print(f"Remove temp file {self.temp.name}", 2)

            os.remove(self.temp.name)

    def verify(self):
        if self.meta["hashmap"] is None:
            self.print(f"Verify file", 2)

            if self.meta["checksum"] != hashlib.sha512(Path(self.meta["filename"]).read_bytes()).hexdigest():
                self.print("[bold yellow]Checksums doesn't match!", 1)

            return

        for filename in self.meta["hashmap"]:
            self.print(f"Verifing {filename}...", 2)
            hashsum = hashlib.sha512(Path(self.exctractDir, filename).read_bytes()).hexdigest()
            
            if hashsum != self.meta["hashmap"][filename]:
                self.print(f"[bold yellow]{filename} checksum doesn't match!", 1)

    def convert(self):
        with self.console.status("[green]Decoding video..."):
            self.writeTempFile()
            self.renameAccordingToMeta()
            self.extract()
            self.verify()

    def print(self, text, verbose):
        if self.verbose >= verbose:
            self.console.print(text)