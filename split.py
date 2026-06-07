import os

filepath = r"c:\Users\lucky\ecommerce-store\app\static\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

style_start = -1
style_end = -1
script_start = -1
script_end = -1

for i, line in enumerate(lines):
    if "<style>" in line and style_start == -1: 
        style_start = i
    elif "</style>" in line and style_start != -1 and style_end == -1: 
        style_end = i
    elif "<script>" in line and script_start == -1 and i > 2000: 
        script_start = i
    elif "</script>" in line and script_start != -1: 
        script_end = i

styles = lines[style_start+1 : style_end]
scripts = lines[script_start+1 : script_end]

with open(r"c:\Users\lucky\ecommerce-store\app\static\styles.css", "w", encoding="utf-8") as f:
    f.writelines(styles)

with open(r"c:\Users\lucky\ecommerce-store\app\static\scripts.js", "w", encoding="utf-8") as f:
    f.writelines(scripts)

new_html = lines[:style_start] + ["    <link rel=\"stylesheet\" href=\"/static/styles.css\">\n"] + lines[style_end+1:script_start] + ["    <script src=\"/static/scripts.js\"></script>\n"] + lines[script_end+1:]

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_html)

print(f"Split completed. CSS lines: {len(styles)}, JS lines: {len(scripts)}, HTML lines: {len(new_html)}")
