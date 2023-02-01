import asyncio


async def handle_echo(reader, writer):
    try:
        data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")
        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()
    except asyncio.TimeoutError:
        print("Timeout error occurred")
    except ConnectionResetError:
        print("Client closed the connection")
    finally:
        writer.close()


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 1234)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


async def client():
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection('127.0.0.1', 1234), timeout=5.0)
        writer.write(b'Hello, World!')
        await writer.drain()
        data = await reader.read(1024)
        print(data.decode())
    except asyncio.TimeoutError:
        print("Timeout error occurred")
    except ConnectionRefusedError:
        print("Server is not available")
    finally:
        writer.close()


if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(client())
