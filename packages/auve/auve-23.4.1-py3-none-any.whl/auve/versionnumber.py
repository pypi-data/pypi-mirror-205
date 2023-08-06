import os

from dataclasses import dataclass
from pathlib import Path

from . import helper


@dataclass
class VersionNumber:
    _date: str = helper.get_date_string()
    _doy: int = helper.get_day_of_year()
    _time: str = helper.get_time_string()

    pri: int = int(_date[2:4])
    sec: int = int(_date[5:7])
    mic: int = 1

    count: int = 1

    build: str = f"{pri}.{_doy:03d}.{_time}"
    release: str = f"{_date}"

    @property
    def full_version(self) -> str:
        return f"version: {self.version_string}, build_{self.count}_{self.build}, release {self.release}"

    @property
    def version_string(self) -> str:
        return f"{self.pri}.{self.sec}.{self.mic}"

    def __str__(self) -> str:
        return self.version_string


@dataclass
class FileContents:
    version: str = VersionNumber().version_string
    build: str = VersionNumber().build
    release: str = VersionNumber().release
    count: str = str(VersionNumber().count)

    @property
    def content(self):
        return self.version, self.build, self.release, str(self.count)


class AutoVersionNumber:
    def __init__(
        self,
        filename: str = None,
        update: bool = False,
    ):
        self.__file = filename
        self.__version_number = VersionNumber()
        self.__root_path = Path(os.getcwd())

        if filename:
            self.__file = self.__root_path.joinpath(filename)
            if not self.__file.is_file():
                self.__write_version_file(self.__file, FileContents())
            else:
                with open(self.__file, "r") as f:
                    lines = f.readlines()

                self.__build_version_number_from_file(lines)

        if update:
            self.update()

    def __build_version_number_from_file(self, content):
        lines = [line.rstrip() for line in content]

        pri, sec, mic = lines[0].split(".")

        self.__version_number.pri = int(pri)
        self.__version_number.sec = int(sec)
        self.__version_number.mic = int(mic)
        self.__version_number.build = lines[1]
        self.__version_number.release = lines[2]
        if len(lines) == 4:
            self.__version_number.count = int(lines[3].strip())
        else:
            self.__version_number.count = int(mic)

    def __update_version(self):
        new = VersionNumber()
        actual = self.__version_number

        self.__version_number.count += 1

        if (new.pri == actual.pri) and (new.sec == actual.sec):
            self.__version_number.mic += 1
        else:
            self.__version_number.mic = 0
            self.__version_number.pri = new.pri
            self.__version_number.sec = new.sec

        return FileContents(
            version=self.__version_number.version_string,
            build=new.build,
            release=new.release,
            count=str(self.__version_number.count),
        )

    def __str__(self):
        return self.__version_number.version_string

    @staticmethod
    def __write_version_file(file: Path, data: FileContents()):
        if not file.parent.exists():
            file.parent.mkdir(parents=True)
        with open(file, "w") as f:
            f.write("\n".join(data.content))

    @property
    def version(self):
        return self.__version_number.version_string

    @property
    def full_version(self):
        return self.__version_number.full_version

    @property
    def build(self):
        return self.__version_number.build

    @property
    def release(self):
        return self.__version_number.release

    @property
    def count(self):
        return self.__version_number.count

    def update(self):
        if self.__file:
            updated = self.__update_version()
            self.__write_version_file(self.__file, updated)
            return True
        else:
            return False
