import tkinter as tk
from .gui import GUI
import asyncio

async def exec():
    window = GUI(asyncio.get_event_loop())
    await window.show()


if __name__ == "__main__":
#    root = tk.Tk()
#    gui = GUI(root)
#    gui.root.mainloop()
    asyncio.run(exec())
