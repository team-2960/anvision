
from linuxpy.video.device import Device, PixelFormat, BufferType, try_format

formats = ["BGR24",
           "BGR32",
           "BGR48_12",
           "BGR666",
           "BGRA32",
           "BGRA444",
           "BGRA555",
           "BGRX32",
           "BGRX444",
           "BGRX555"]

if __name__ == '__main__':
    with open('/dev/video0', 'r') as f:
        for format in PixelFormat:
            result = try_format(f, BufferType.VIDEO_CAPTURE, 1280, 720, format)
            print(f"Format: {format.name} - Result: {result}")


