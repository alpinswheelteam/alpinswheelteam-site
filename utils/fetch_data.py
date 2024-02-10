import pandas as pd
import json

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR054bKX_g-UGoIV-YAlsPUX0Lpz9OA-Na0DqWNi1ixzFFQ4AUE6wJVuFqFUTX9Tt04pyJJF7yJfWYb/pub?gid=378471329&single=true&output=csv"
table = pd.read_csv(url)
table["DATE"] = pd.to_datetime(table["DATE"], format="mixed")
table_filtered = table[table["DATE"] < pd.Timestamp.now() + 4 * pd.offsets.Week()]
table_filtered = table_filtered.set_index("NOM")
table_sorted = table_filtered.sort_values("DATE")

result = []
for nom in table_sorted.index:
    result.append({"nom": nom, "date": str(table_sorted["DATE"][nom].date()), "course": table_sorted["COURSE"][nom]})

json.dump({"courses": result}, open("test.json", "w"), indent=4, ensure_ascii=False)