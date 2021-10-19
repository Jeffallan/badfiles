from functools import partial
from typing import Generator


def process_tar(f, chunk: int = 512) -> Generator[bytes, None, None]:

    with open(f, "rb") as f:
        for fh in iter(partial(f.read, chunk), b""):
            try:
                data = fh
                # size = data.decode("ascii")[124:135]
                # print(size)
                if data.decode("ascii")[257:262] == "ustar" and data[125:135].isascii():
                    yield data
            except (UnicodeDecodeError, ValueError):
                pass


if __name__ == "__main__":
    print([p for p in process_tar("./test/tar_dir.tar")])
