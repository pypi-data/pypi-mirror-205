
if __name__ == "__main__":
    from digiDownload import run
    from asyncio import run as run_async
    run_async(run())
    exit(0)

from digiDownload import Session
import digiDownload.exceptions as exceptions
