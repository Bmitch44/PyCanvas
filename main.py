"""
testing if i can wirte .canvas files to obsidian vault
"""

from canvas import Canvas

path_to_vault = "/Users/bradymitchelmore/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal/Personal/"

# create a new canvas file and save it to the vault
canvas = Canvas(path_to_vault)
node1_id = canvas.add_node(node_type='text', text='Hello World!', x=100, y=100, width=100, height=100)
node2_id = canvas.add_node(node_type='text', text='Hello World!', x=150, y=150, width=100, height=100)
node3_id = canvas.add_node(node_type='file', filename="test.md", text='testing', x=200, y=200, width=100, height=100)

# Now you can use these IDs to create an edge
canvas.add_edge('directional', node1_id, 'right', node2_id, 'left')

# Save the canvas to a file
canvas.save_to_file(f'test.canvas')
