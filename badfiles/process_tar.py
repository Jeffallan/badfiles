from functools import partial


def process_tar(f, header: int = 500):

    with open(f, "rb") as f:
        for fh in iter(partial(f.read, header), b""):
            try:
                data = fh
                size = data.decode("ascii")[124:135]
                size_dec = int(size, 8)
                seek = (
                    size_dec + header + 477
                )  # + size_dec % 512 #+ 500 if size_dec % 512 == 0 else size_dec + 500 + 512 - 35 #35?
                f.seek(seek)
                print(data)
                print("Next Position:", f.tell(), hex(f.tell()), sep="\t")
                print("Size:", size, int(size, 8), sep="\t")
                # data = f.read(fh)
                # print(data)
            except (UnicodeDecodeError, ValueError):
                pass


if __name__ == "__main__":
    process_tar("./test/mult.tar")
