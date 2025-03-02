from pwn import remote
from src.logger import get_logger
import threading

log = get_logger(__name__)

packets = []

def receive_messages(r):
    while True:
        try:
            # Пытаемся принять данные (timeout можно настроить по необходимости)
            data = r.recv(timeout=1)
            if data:
                message = data.decode('utf-8', errors='ignore')
                print(f"[Server]: {message}", end="")
                packets.append({"sender": "server", "data": message})
        except EOFError:
            log.info("Connection closed by server.")
            break
        except Exception as e:
            log.error("Error while receiving data:", e)
            break

def start_catching(host: str, port: int):
    try:
        r = remote(host, port)
        log.info(f"Connected to {host}:{port}")
    except Exception as e:
        log.error("Failed to connect:", e)
        return

    recv_thread = threading.Thread(target=receive_messages, args=(r,))
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while True:
            user_input = input("Enter message (or 'exit' to exit): ")
            if user_input.lower() == 'exit':
                log.info("Exiting...")
                break

            r.sendline(user_input)
            packets.append({"sender": "user", "data": user_input})
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
    finally:
        r.close()

    # Вывод всех записанных пакетов
    log.debug(f"\nRecorded packets: {packets}")
    return packets
