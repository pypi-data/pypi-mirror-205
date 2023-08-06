import hashlib


def md5_encode(data: str, salt: str):
    m = salt + '%' + data + '$' + salt
    return hashlib.md5(m.encode(encoding='utf-8')).hexdigest()


if __name__ == "__main__":
    print(md5_encode("hello", "tiny"))