#!/usr/bin/env python3
cmt_file = "data/cmtsolution"

with open(cmt_file, 'r') as file:
    content = file.read()

content = content.replace('19.3000', '10.0000').replace(' 0.6', '10.0').replace("PDEQ", "PDE")

with open(cmt_file, 'w') as file:
    file.write(content)

print(f"Modified file saved as {cmt_file}")

