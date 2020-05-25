find = "</header>"
link = "https://github.com/barischrooneyj/bridge-sim#concrete-slab-bridge-simulation-"
replace = (
    f"This is the API documentation.<br><br>"
    f"The project homepage is <a href='{link}'>here</a>."
)
with open("docs/index.html") as f:
    file = f.read()
file = file.replace(find, find + replace)
with open("docs/index.html", "w") as f:
    f.write(file)
