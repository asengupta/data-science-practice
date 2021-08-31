import regex

f = open("../data/data_description.txt")
text = f.read()

# print(text)
# compiled = regex.compile("((.+?): (.+?)\n+(^\s+(.+?)\t(.+?)$\n)+\s+)+")
# compiled = re.compile("(.+?): (.+?)\n+(|^\s+(.+?)\t(.+?)|$\n)+")
# searched = regex.match(r"((.+?): (.+?)\n+(\s+([A-Za-z0-9&]+)\s+(.+?)\n+)*)+", text)
searched = regex.match(r"((.+?): (.+?)\n+(\s+[A-Za-z0-9&.]+\s+(.*)\n+)*)+", text)
# searched = regex.match(r"([^(.+?): (.+?)\n+]+)", text)
# print(searched.groups())
# print(searched.captures(1))
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
    # print(values)
    metadata.append({"name": variable, "meaning": meaning, "values": values})
    # print(segment)
    # print(len(segments))
    # for idx, val in enumerate(variables):
    #     dictionary[val] = {"meaning": meanings[idx], "values": []}
    #     decomposed_category = regex.match(r"\s+([A-Za-z0-9&.]+)\s+(.*)|$", categories[idx])

    # categories = category_matches.captures(3)
    # for idx, category in enumerate(categories):
    #     print(f"Category is {category}")
    #     decomposed_category = regex.match(r"\s+([A-Za-z0-9&.]+)\s+(.*)|$", category)
    #     # dictionary[val]["values"].append({"name": decomposed_category.captures(1)[0], "meaning": decomposed_category.captures(2)[0]})
    #     print(decomposed_category.captures(1)[0])
    #     print(decomposed_category.captures(2)[0])

print(metadata)
