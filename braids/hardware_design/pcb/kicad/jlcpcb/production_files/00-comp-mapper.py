import csv
import collections
import json

# * export BOM with KiCad plugin.
# * run this script which:
#   * reads a GOOD file of known-good jlc_components.
#   * reads the BOM from the plugin.
#   * writes a NEW-BOM with the known-good jlc_components joined in.

# local_designators:
#   (r0603, 100k): [r1, r2, r3]
local_designators = collections.defaultdict(list)

# jlc_components:
#   (r0603, 100k): c123
jlc_components = collections.defaultdict(list)

GOOD_FILE = "braids-good.csv"
EMPTY_BOM_FILE = "BOM-braids.csv"
NEW_BOM_FILE = "NEW-BOM-braids.csv"

with open(GOOD_FILE) as f:
    reader = csv.DictReader(f, delimiter=";", quotechar='"')
    for row in reader:
        if row["LCSC"] != "part selected":
            key = (row["Footprint"], row["Comment"])
            new_desc = [row["LCSC"], row["Description"]]

            if key in jlc_components:
                if jlc_components[key] != new_desc:
                    import pdb; pdb.set_trace()
                    raise Exception("disagree")
            else:
                jlc_components[key] = new_desc


with open(EMPTY_BOM_FILE) as f:
    reader = csv.DictReader(f, delimiter=",", quotechar='"')
    for row in reader:
        key = (row["Footprint"], row["Comment"])
        local_designators[key] += row["Designator"].split(",")


# print(json.dumps(local_designators, indent=2))
# print(json.dumps(jlc_components, indent=2))


with open(NEW_BOM_FILE, "w") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Footprint", "Designator", "Comment", "LCSC", "Description"])
    for (package, value), desis in sorted(local_designators.items()):
        # print("(%s, %s): %s" % (package, value, jlc_components[(package, value)]))
        jlc_comps = jlc_components[(package, value)] or ["", ""]
        writer.writerow([
            package,
            ",".join(sorted(desis)),
            value,
            jlc_comps[0],
            jlc_comps[1]
        ])

