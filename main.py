"""
testing if i can wirte .canvas files to obsidian vault
"""

from canvas import Canvas

path_to_vault = "/Users/bradymitchelmore/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal/Personal"

# create a new canvas file and save it to the vault
canvas = Canvas()
canvas.add_node("text", text="Hello World!", x=100, y=100, width=100, height=100)
canvas.save_to_file(f"{path_to_vault}/test.canvas")