from pathlib import Path

from abc import ABC, abstractmethod
from schemas import OutputType, SessionEvents
import json
from typing import Dict, List, TYPE_CHECKING, Any
import shutil
import utils
import os
from message import messages
from datetime import datetime
import zipfile
from typing import Callable

if TYPE_CHECKING:
    from session import Session  # for static checking only


class DirectoryValidator(ABC):
    def __init__(
        self,
        path: Path,
        allowed_subfolders: list[str],
        allowed_files: Dict[str, List[str]],
    ):
        self.path = path
        self.allowed_subfolders = allowed_subfolders
        self.allowed_files = allowed_files

    @abstractmethod
    def validate(self):
        pass

    def extension(self, file: Path = None) -> str:
        if file is None:
            return self.path.suffix.lower()
        return file.suffix.lower()

    def name(self, file: Path = None) -> str:
        if file is None:
            return self.path.name.removesuffix(self.path.suffix)
        return file.name.removesuffix(file.suffix)

    def extension_allowed(self, fname: str, fext: str) -> bool:
        for file in self.allowed_files.keys():
            if (file == fname) and (fext in self.allowed_files[file]):
                return True
        return False


class AssetDirectoryValidator(DirectoryValidator):

    def __init__(self, path: Path):
        super().__init__(path, [], self.allowed_files)

    def validate(self):
        if not self.path.is_dir():
            return False
        for file in iter(self.path.iterdir()):
            if file.is_dir():
                if (
                    len(self.allowed_subfolders) > 0
                    and file.name not in self.allowed_subfolders
                ):
                    return False
            if file.is_file() and not self.extension_allowed(
                self.name(file), self.extension(file)
            ):
                return False
        return True


class RootDirectoryValidator(DirectoryValidator):
    def __init__(self, path: Path):
        super().__init__(
            path,
            ["tracks", "sfx", "interrupts"],
            {
                "metadata": [".json"],
                "cover": [".png", ".gif"],
                "intro": [".mp3"],
                "README": [".md"],
            },
        )

    def is_hidden_file(path: Path):
        return path.name.startswith(".") or ".DS_Store" in path.name

    def validate(self):
        if not self.path.is_dir():
            return False
        for file in iter(self.path.iterdir()):
            if RootDirectoryValidator.is_hidden_file(file):  # ignore hidden files
                continue
            if file.is_dir() and file.name not in self.allowed_subfolders:
                utils.type_line(f'subfolder "{file.name}" is not allowed', 0.04)
                return False
            if file.is_file() and not self.extension_allowed(
                self.name(file), self.extension(file)
            ):
                utils.type_line(
                    f'file extension "{self.extension(file)}" is not allowed in file "{self.name(file)}"',
                    0.04,
                )
                return False
        return True


class TempTree:

    _path = Path("temp")
    _temp = {
        "tracks": _path / "tracks",
        "sfx": _path / "sfx",
        "interrupts": _path / "interrupts",
        "metadata": _path / "metadata.json",
        "cover": _path / "cover.png",
        "gif": _path / "cover.gif",
        "intro": _path / "intro.mp3",
        "readme": _path / "README.md",
    }

    def __init__(self):
        return 

    def tracks():
        return [
            (TempTree._temp["tracks"] / file.name)
            for file in (TempTree._temp["tracks"]).iterdir()
            if not RootDirectoryValidator.is_hidden_file(file)
        ]

    def sfx():
        return [
            (TempTree._temp["sfx"] / file.name)
            for file in (TempTree._temp["sfx"]).iterdir()
            if not RootDirectoryValidator.is_hidden_file(file)
        ]

    def interrupts():
        return [
            (TempTree._temp["interrupts"] / file.name)
            for file in (TempTree._temp["interrupts"]).iterdir()
            if not RootDirectoryValidator.is_hidden_file(file)
        ]

    def metadata(as_dict: bool = False):
        if as_dict:
            return json.loads((TempTree._temp["metadata"]).read_text())
        return TempTree._temp["metadata"]

    def write_metadata(data: dict):
        (TempTree._temp["metadata"]).write_text(json.dumps(data))

    def has_cover():
        return (TempTree._temp["cover"]).exists() or (TempTree._temp["gif"]).exists()

    def cover():
        return (
            TempTree._temp["cover"]
            if (TempTree._temp["cover"]).exists()
            else TempTree._temp["gif"]
        )

    def has_intro():
        return (TempTree._temp["intro"]).exists()

    def intro():
        return TempTree._temp["intro"]

    def readme():
        return TempTree._temp["readme"]

    def has_readme():
        return TempTree._temp["readme"].exists()

    def has_metadata():
        return TempTree._temp["metadata"].exists()

    def list_files():
        files: List[Path] = TempTree.tracks() + TempTree.sfx() + TempTree.interrupts()
        if TempTree.has_metadata():
            files.append(TempTree.metadata())
        if TempTree.has_cover():
            files.append(TempTree.cover())
        if TempTree.has_intro():
            files.append(TempTree.intro())
        if TempTree.has_readme():
            files.append(TempTree.readme())
        return files

    def walk(actions: Callable[[Path], Any]):
        for path in TempTree.tracks():
            yield actions(path)
        for path in TempTree.sfx():
            yield actions(path)
        for path in TempTree.interrupts():
            yield actions(path)
        if TempTree.has_metadata():
            yield actions(TempTree.metadata())
        if TempTree.has_cover():
            yield actions(TempTree.cover())
        if TempTree.has_intro():
            yield actions(TempTree.intro())
        if TempTree.has_readme():
            yield actions(TempTree.readme())
        return

class ProcessedResponse:
    def __init__(self, valid: bool, error: str, path: Path):
        self.valid = valid
        self.error = error
        self.path = path
        return

class FileHandler:

    def __init__(self):
        return

    def list_files(path: Path):
        files = []
        for path in path.iterdir():
            files.append(path.name)
        return files

    def calc_total_pak_size(path: Path):
        total_size = 0
        for path in TempTree.walk(FileHandler.file_size_mb):
            total_size += path
        return total_size

    def process_file(candidate_path: str=None):
        if not candidate_path:
            return ProcessedResponse(
                valid=False,
                error="No file provided",
                path=None
            )
        path = Path(candidate_path.strip('"').strip("'"))

        if path.is_file():
            return ProcessedResponse(
                valid=False,
                error=f"File {path} is not a directory",
                path=None
            )
        elif path.is_dir():
            if FileHandler.is_valid_candidate(path):
                return ProcessedResponse(
                    valid=True,
                    error=None,
                    path=path
                )
            else:
                return ProcessedResponse(
                    valid=False,
                    error=f"Invalid directory {path}",
                    path=path
                )
        else:
            return ProcessedResponse(
                valid=False,
                error=f"File {path} does not exist",
                path=path
            )

    # def handle_file_dropped(self, file: str = None):
    #     if not file:
    #         return
    #     path = file.strip('"').strip("'")
    #     self._path = Path(path)

    #     if self._path.is_file():
    #         return False
    #         # utils.type_text("[Error] Invalid file type", OutputType.error)
    #         # utils.type_text(
    #         #     messages["start_prompt"], OutputType.question, self.handle_file_dropped
    #         # )
    #     elif self._path.is_dir():
    #         if self.is_valid_candidate(self._path):
    #             self.copy_to_temp()
    #             total_pak_size = FileHandler.calc_total_pak_size()
    #             if total_pak_size > 10:
    #                 self.session.io.write(
    #                     """
    #                 -----------------------------------------------------------------------------
    #                 |                                                                            |
    #                 | PAK size exceeds the 10MB limit ~ ({total_pak_size}MB)                     |
    #                 | Drop in a smaller pak or select prune to drop selected files               |
    #                 |                                                                            |
    #                 -----------------------------------------------------------------------------
    #                 """,
    #                     OutputType.text,
    #                 )
    #                 self.session.io.write(
    #                     messages["default_mode_prompt"],
    #                     OutputType.question,
    #                     self.handle_file_dropped,
    #                 )
    #             self.session.events.emit(SessionEvents.pak_validated)
    #         else:
    #             self.session.io.write(
    #                 "[Error] Invalid directory. Please drag and drop a valid PAK structured directory. Visit https://github.com/k0ruption/nerapakker for more information.",
    #                 OutputType.error,
    #             )
    #             self.session.io.write(
    #                 messages["start_prompt"],
    #                 OutputType.question,
    #                 self.handle_file_dropped,
    #             )
    #     else:
    #         self.session.io.write(f"[Error] Invalid path: {path}", OutputType.error)
    #         self.session.io.write(
    #             messages["start_prompt"], OutputType.question, self.handle_file_dropped
    #         )

    def copy_to_temp(path: Path):
        # for path in path.iterdir():
        #     utils.type_line(f"Copying {path} into temp", 0.04)
        shutil.copytree(path, "temp", dirs_exist_ok=True)

    def is_valid_candidate(folder: Path):
        return RootDirectoryValidator(folder).validate()

    def clear_temp():
        for path in TempTree.tracks():
            path.unlink()
        for path in TempTree.sfx():
            path.unlink()
        for path in TempTree.interrupts():
            path.unlink()

        if TempTree.has_metadata():
            TempTree.metadata().unlink()
        if TempTree.has_cover():
            TempTree.cover().unlink()
        if TempTree.has_intro():
            TempTree.intro().unlink()
        if TempTree.has_readme():
            TempTree.readme().unlink()

    def pak_temp(pak_name: str):
        with zipfile.ZipFile(
            pak_name + ".pak", "w", zipfile.ZIP_DEFLATED
        ) as pak:
            pak.write(TempTree.metadata(), arcname="metadata.json")
            if TempTree.has_cover():
                pak.write(TempTree.cover(), arcname="cover.png")
            if TempTree.has_intro():
                pak.write(TempTree.intro(), arcname="intro.mp3")
            if TempTree.has_readme():
                pak.write(TempTree.readme(), arcname="README.md")
            pak.mkdir("tracks")
            pak.mkdir("sfx")
            pak.mkdir("interrupts")
            for track in TempTree.tracks():
                pak.write(track, arcname=f"tracks/{track.name}")
            for sfx in TempTree.sfx():
                pak.write(sfx, arcname=f"sfx/{sfx.name}")
            for interrupt in TempTree.interrupts():
                pak.write(interrupt, arcname=f"interrupts/{interrupt.name}")

    def is_file_empty(path: Path):
        return path.exists() and path.stat().st_size == 0

    def is_dir_empty(path: Path):
        return path.exists() and not any(path.iterdir())

    def file_size_mb(path: Path):
        size_bytes = os.path.getsize(path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
