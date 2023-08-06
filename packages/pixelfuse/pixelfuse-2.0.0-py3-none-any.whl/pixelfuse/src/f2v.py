import hashlib
import os
from pathlib import Path
import pickle
import struct

import cv2
import numpy as np
from rich import print
from rich.progress import (BarColumn, MofNCompleteColumn, Progress,
                           SpinnerColumn, TimeElapsedColumn,
                           TimeRemainingColumn)

from pixelfuse import encoder


class ToVideo(object):
    def __init__(self, file: Path, fps=1., width=640, height=480, fourcc="HFYU", output: Path=Path("output.avi"), verbose=2, hashmap=None):
        self.file = file
        self.fps = fps
        self.width = width
        self.height = height
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.output = output
        self.checksum = hashlib.sha512(self.file.read_bytes()).hexdigest()
        self.verbose = verbose
        self.hashmap = hashmap

        self.bytesInFile = self.file.stat().st_size
        self.pixelsInFile = (self.bytesInFile//3)+1

        self.barColumns = [
            SpinnerColumn(),
            "{task.description}",
            BarColumn(),
            "Elapsed time:",
            TimeElapsedColumn(),
            "Remaining time:",
            TimeRemainingColumn(),
            "Completed pixels:",
            MofNCompleteColumn()
        ]
        self.barKwargs = {
            "transient": True
        }

    def convert(self):
        out = cv2.VideoWriter(self.output.name, self.fourcc, self.fps, (self.width, self.height))

        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.print("Opening the file...", 1)
        with self.file.open("rb") as f:
            y = 0
            x = 0
            self.print("Creating meta data...", 2)
            meta = {
                "checksum": self.checksum,
                "filename": self.file.name,
                "encoder": encoder,
                "lastZeros": 0,
                "hashmap": self.hashmap
            }

            self.print("Starting video writing...", 1)
            with Progress(*self.barColumns, **self.barKwargs) as progress:
                for i in progress.track(range(self.pixelsInFile)):
                    b = f.read(3)
                    if not b:
                        self.print("File end", 3)
                        break
                    if len(b) < 3:
                        meta["lastZeros"] = 3-len(b)
                        self.print(f"File end with {meta['lastZeros']} left zeros", 3)
                        b = b.ljust(3, b'\x00')

                    frame[y, x] = struct.unpack('<BBB', b)
                    x += 1
                    if x >= self.width:
                        x = 0
                        y += 1
                    if y >= self.height:
                        self.print(f"Done {frame[0, 0]} frame", 2)
                        out.write(frame)
                        y = 0
                        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

                if np.any(frame):
                    self.print(f"Writing not full {frame[0, 0]} frame", 2)
                    out.write(frame)

                self.print(f"Creating meta data frame...", 3)
                pickle_bytes = pickle.dumps(meta)
                frame = np.frombuffer(pickle_bytes, dtype=np.uint8).copy()
                frame.resize((self.height, self.width, 3))

                self.print(f"Writing meta data {frame[0, 0]} frame", 2)
                out.write(frame)

        self.print(f"Writing video...", 1)
        out.release()

    def print(self, text, verbose):
        if self.verbose >= verbose:
            print(text)