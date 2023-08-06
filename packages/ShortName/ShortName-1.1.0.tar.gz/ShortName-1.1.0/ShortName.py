import ctypes
import argparse
import sys


def error(message: str, exit_code: int):
    print(message, file=sys.stderr)
    sys.exit(exit_code)


if not hasattr(ctypes, "windll"):
    error("windll is not available. The program cannot continue.", 1)


def main():
    parser = argparse.ArgumentParser(description="set or view the shortname of a file")
    subparsers = parser.add_subparsers(dest="action", metavar="set|get")
    setter = subparsers.add_parser(
        "set", aliases=("s",), help="modify the shortname of a file"
    )
    setter.add_argument(
        "-q", "--quiet", action="store_true", help="hide output on success"
    )
    setter.add_argument("file", help="file whose shortname should be modified")
    setter.add_argument(
        "name",
        help=(
            "shortname to set on the file."
            " Must have 8 or fewer characters before the file extension,"
            " and no spaces."
        ),
    )
    getter = subparsers.add_parser(
        "get", aliases=("g",), help="query the shortname of a file"
    )
    getter.add_argument("file", help="file whose shortname should be queried")
    args = parser.parse_args()

    if args.action == "set":
        try:
            file = WinFile(lpFileName=args.file)
        except OSError:
            error(f"Could not open file: {args.file}", 2)

        try:
            file.set_short_name(args.name)
            if not args.quiet:
                print(f'Successfully set shortname of {args.file} to "{args.name}"')
        except OSError:
            error(f'Could not set shortname to "{args.name}"', 2)
        finally:
            file.close()
    elif args.action == "get":
        try:
            print(WinFile.get_short_name(lpszLongPath=args.file))
        except OSError:
            error(f"Could not retrieve shortname for file: {args.file}", 2)


class WinFile:
    # Win32 constants
    DELETE = 0x00010000
    FILE_SHARE_DELETE, FILE_SHARE_WRITE, FILE_SHARE_READ = 0x4, 0x2, 0x1
    NULL = 0
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    INVALID_HANDLE = -1
    MAX_PATH = 260

    def __init__(
        self,
        lpFileName: str,
        dwDesiredAccess=DELETE,
        dwShareMode=FILE_SHARE_DELETE | FILE_SHARE_WRITE | FILE_SHARE_READ,
        lpSecurityAttributes=NULL,
        dwCreationDisposition=OPEN_EXISTING,
        dwFlagsAndAttributes=FILE_FLAG_BACKUP_SEMANTICS,
        hTemplateFile=NULL,
    ):
        # To change the short name of a file later, it must be opened with either:
        # 1. dwDesiredAccess=GENERIC_ALL, or
        # 2. dwDesiredAccess=DELETE and dwFlagsAndAttributes=FILE_FLAG_BACKUP_SEMANTICS
        # FILE_FLAG_BACKUP_SEMANTICS is necessary for opening directories anyway,
        # so this defaults to the latter option.

        # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
        self.handle = ctypes.windll.kernel32.CreateFileW(
            self.get_long_path(lpFileName),
            dwDesiredAccess,
            dwShareMode,
            lpSecurityAttributes,
            dwCreationDisposition,
            dwFlagsAndAttributes,
            hTemplateFile,
        )

        if self.handle == self.INVALID_HANDLE:
            raise OSError()

    @classmethod
    def get_long_path(cls, path: str):
        if len(path) + 1 > cls.MAX_PATH and not path.startswith("\\\\?\\"):
            return f"\\\\?\\{path}"
        else:
            return path

    def close(self):
        # https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
        ctypes.windll.kernel32.CloseHandle(self.handle)

    @classmethod
    def get_short_name(cls, lpszLongPath: str):
        # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getshortpathnamew
        buffer_size: int = ctypes.windll.kernel32.GetShortPathNameW(
            lpszLongPath, cls.NULL, 0
        )
        if buffer_size == 0:
            raise OSError()

        buffer = ctypes.create_unicode_buffer(buffer_size)
        name_length = ctypes.windll.kernel32.GetShortPathNameW(
            lpszLongPath, buffer, buffer_size
        )

        if name_length == 0 or name_length != buffer_size - 1:
            raise OSError()
        else:
            return buffer.value

    def set_short_name(self, name: str):
        # https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setfileshortnamew
        if ctypes.windll.kernel32.SetFileShortNameW(self.handle, name) == 0:
            raise OSError()


if __name__ == "__main__":
    main()
