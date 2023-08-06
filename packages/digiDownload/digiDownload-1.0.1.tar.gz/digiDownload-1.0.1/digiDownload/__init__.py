
if __name__ == "__main__":
    from cli_tool import run
    from asyncio import run as run_async
    run_async(run())
    exit(0)

import Session
import exceptions
