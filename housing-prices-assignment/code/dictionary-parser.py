import regex

f = open("../data/data_description.txt")
text = f.read()

searched = regex.match(r"((.+?): (.+?)\n+(\s+[A-Za-z0-9&.]+\s+(.*)\n+)*)+", text)
segments = searched.captures(1)
print(segments)

metadata = []
for segment in segments:
    category_matches = regex.match(r"(.+?): (.+?)\n+(\s+[A-Za-z0-9&.]+\s+(.*)\n+)*", segment)
    variable = category_matches.captures(1)[0]
    meaning = category_matches.captures(2)[0]
    # print(f"{variable}-{meaning}")
    categories = category_matches.captures(3)
    values = []
    for category in categories:
        decomposed_category = regex.match(r"\s+([A-Za-z0-9&.]+)\s+(.*)|$", category)
        values.append({"value": decomposed_category.captures(1)[0], "meaning": decomposed_category.captures(2)[0]})
    metadata.append({"name": variable, "meaning": meaning, "values": values})
print(metadata)
