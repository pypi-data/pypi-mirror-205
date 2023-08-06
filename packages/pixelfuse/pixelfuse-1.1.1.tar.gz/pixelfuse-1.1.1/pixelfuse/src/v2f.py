import cv2 
import pickle
import numpy as np
import tempfile
import os
import hashlib
from rich.console import Console
from pixelfuse import decoder, compatible_encoders

class ToFile:
    def __init__(self, filename, verbose):
        self.cap = cv2.VideoCapture(filename)
        self.console = Console()
        self.verbose = verbose

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
        try:
            self.print(f"Rename temp file: {self.temp.name} -> ./{self.meta['filename']}", 1)
            os.link(self.temp.name, self.meta["filename"])
        except FileExistsError:
            os.remove(self.temp.name)
            raise FileExistsError(f"Cannot write file, file already exists: {self.meta['filename']}")

        self.print(f"Remove temp file {self.temp.name}", 2)
        os.remove(self.temp.name)

    def verify(self):
        self.print(f"Verify file", 2)
        if self.meta["checksum"] != hashlib.sha512(open(self.meta["filename"], 'rb').read()).hexdigest():
            print("Doesn't match")

    def convert(self):
        with self.console.status("[green]Decoding video..."):
            self.writeTempFile()
            self.renameAccordingToMeta()
            self.verify()

    def print(self, text, verbose):
        if self.verbose >= verbose:
            self.console.print(text)