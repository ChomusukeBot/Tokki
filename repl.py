import aiomonitor
import asyncio


def main():
    """
    Functions that launches the asynchronous REPL.
    """
    # Get the current event loop
    loop = asyncio.get_event_loop()
    # While the moonitor is running
    with aiomonitor.start_monitor(loop=loop):
        # Keep the loop working
        loop.run_forever()


if __name__ == "__main__":
    main()
