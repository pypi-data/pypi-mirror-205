from . UI import functions as UI
from asyncio import run

UI.banner()
try:
    run(UI.run())
except Exception as e:
    print(e)
