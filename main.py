"""
testing if i can wirte .canvas files to obsidian vault
"""

from canvas import Canvas

path_to_vault = "/Users/bradymitchelmore/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal/Personal/"

# create a new canvas file and save it to the vault
canvas = Canvas(path_to_vault)
node1_id = canvas.add_node(node_type='text', text='Hello World!')
node2_id = canvas.add_node(node_type='text', text='Hello World!')
node3_id = canvas.add_node(node_type='file', filename="test.md", text='testing', width=200, height=200)

# Now you can use these IDs to create an edge
canvas.add_edge('directional', node1_id, 'right', node2_id, 'left')
canvas.add_edge('directional', node1_id, 'right', node3_id, 'left')

# create a group node
group_id = canvas.add_node(node_type='group', children=[node1_id, node2_id], label='group')

# Save the canvas to a file
canvas.save_to_file(f'test.canvas')
