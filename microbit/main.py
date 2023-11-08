import radio
import microbit

radio.on()

radio.config(length=251, queue=8, power=7)

microbit.uart.init(115200)

system_id = 0

uart_buffer = b""

while True:
    if microbit.uart.any():
        uart_bytes = microbit.uart.read()
        if uart_bytes:
            uart_buffer += uart_bytes
            
        if b"!c" in uart_buffer:
            uart_buffer = b""
            
        if b"!r" in uart_buffer:
            command_index = uart_buffer.index(b"!r")
            if command_index >= 0:
                system_id = uart_buffer[command_index-1]
            uart_buffer = uart_buffer[command_index+2:]

        if b"!s" in uart_buffer:
            command_index = uart_buffer.index(b"!s")
            radio.send_bytes(uart_buffer[:command_index])
            uart_buffer = uart_buffer[command_index+2:]
            
    radio_bytes = radio.receive_bytes()
    if radio_bytes:
        if radio_bytes[0] == system_id:
            microbit.uart.write(radio_bytes)
        elif radio_bytes[1] > 0:
            radio.send_bytes(
                bytes(radio_bytes[0])+bytes(radio_bytes[1]-1)+radio_bytes[2:]
            )
            microbit.uart.write("Routed for another mb")
