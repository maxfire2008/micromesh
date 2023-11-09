import serial
import sys


def main():
    ser = serial.Serial(sys.argv[1], 115200)

    # register system id
    ser.write(bytes([int(sys.argv[2])]) + b"!r")

    while True:
        command = input(">")
        if command == "exit":
            break
        if command == "send":
            ser.write(
                bytes([int(input("DEST>"))])
                + bytes([int(sys.argv[2])])
                + b"\xff"
                + input("DATA>").encode("utf-8")
                + b"!s"
            )
        if command == "recv":
            # read serial connection
            while ser.in_waiting:
                print(ser.read(ser.in_waiting))


if __name__ == "__main__":
    main()
