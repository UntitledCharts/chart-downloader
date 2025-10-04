from typing import Union
from pathlib import Path


def _read_start(path: Union[str, Path], n: int = 64) -> bytes:
    p = Path(path)
    with p.open("rb") as f:
        return f.read(n)


def detect_image(path: Union[str, Path]) -> str:
    """
    Detect image type by header bytes.
    Returns: 'png', 'jpg', or 'unknown'
    """
    data = _read_start(path, 32)
    if not data:
        return "unknown"

    # PNG: 89 50 4E 47 0D 0A 1A 0A
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    # JPEG: Start Of Image 0xFF 0xD8 ... often followed by 0xFF 0xE0 (JFIF) or 0xFF 0xE1 (Exif),
    # but many valid jpegs simply start with 0xFF 0xD8 0xFF.
    if data.startswith(b"\xFF\xD8\xFF"):
        return "jpg"

    # Some JPEGs include 'JFIF' or 'Exif' within the first 32 bytes
    if b"JFIF" in data[:32] or b"Exif" in data[:32]:
        return "jpg"

    return "unknown"


def detect_audio(path: Union[str, Path]) -> str:
    """
    Detect audio type by header bytes.
    Returns: 'mp3', 'wav', 'ogg', or 'unknown'
    """
    data = _read_start(path, 64)
    if not data:
        return "unknown"

    # WAV: "RIFF" at 0 and "WAVE" at offset 8
    if len(data) >= 12 and data[0:4] == b"RIFF" and data[8:12] == b"WAVE":
        return "wav"

    # Ogg: "OggS" at start
    if data.startswith(b"OggS"):
        return "ogg"

    # MP3: common indicators:
    #  - ID3 tag at start (ID3v2)
    #  - Frame sync: first 11 bits set => first byte 0xFF and next byte with top 3 bits 0b111 (0xE0 mask)
    if data.startswith(b"ID3"):
        return "mp3"
    if len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0:
        # This looks like an MPEG audio frame header (typical for MP3 without ID3)
        return "mp3"

    return "unknown"


# tests
if __name__ == "__main__":
    import tempfile

    samples = {
        "png": b"\x89PNG\r\n\x1a\n" + b"\x00" * 20,
        "jpg": b"\xFF\xD8\xFF\xE0" + b"\x00" * 20,
        "wav": b"RIFF" + b"\x00\x00\x00\x00" + b"WAVE" + b"\x00" * 20,
        "ogg": b"OggS" + b"\x00" * 20,
        "mp3_id3": b"ID3" + b"\x00" * 20,
        "mp3_frame": b"\xFF\xFB" + b"\x00" * 20,
        "unknown": b"NOTKNOWN" + b"\x00" * 20,
    }

    for name, content in samples.items():
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(content)
            tf.flush()
            path = tf.name
        if name in ("png", "jpg", "unknown"):
            print(name, "->", detect_image(path))
        else:
            print(name, "->", detect_audio(path))
