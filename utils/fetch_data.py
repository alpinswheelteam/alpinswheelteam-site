import pandas as pd
import json
import numpy as np 
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR054bKX_g-UGoIV-YAlsPUX0Lpz9OA-Na0DqWNi1ixzFFQ4AUE6wJVuFqFUTX9Tt04pyJJF7yJfWYb/pub?gid=1022985253&single=true&output=csv"
df = pd.read_csv(url, index_col=0).T
df.pop(df.columns[-1])

now = pd.Timestamp.now()
df["DATE"] = pd.to_datetime(df["DATE"], format="%d/%m", errors="coerce")
df["DATE"] = df["DATE"].apply(lambda x: x.replace(year = now.year))

df = df[:-8]
df = df[df["DATE"] < pd.Timestamp.now() + 3 * pd.offsets.Week()]
df = df.sort_values("DATE")
df = df[:4]

membres_site = json.load(open("data/membres.json"))["membres"]

result = {}
for index, row in df.iterrows():
    selection = row[5:]
    coureurs = selection.keys()
    choix = selection.values.astype(str)
    
    coureurs = coureurs[choix != "nan"]
    coureurs_formatted = []
    if len(coureurs) == 0:
        continue
    for coureur in coureurs:
        nom, prenom = coureur.split()
        nom = nom.lower().capitalize()
        prenom = prenom.lower().capitalize()
        coureur_fmt = f"{prenom} {nom}"
        found = False
        for x in membres_site:
            if coureur_fmt.replace("é", "e") == x["nom"].replace("é", "e"):
                found = True
                coureurs_formatted.append(
                    {"nom": x["nom"],
                     "image": x["image"],
                    }
                )
                break
        if not found:
            coureurs_formatted.append(
                    {"nom": coureur_fmt,
                     "image": "/images/alphin_logo.png",
                    }
                )
       
    course = index
    federation = row["FEDERATION"]
    departement = row["COMITE"]
    date = str(row["DATE"].date())
    result[course] = {
        "date": date,
        "departement": departement,
        "federation": federation,
        "coureurs": coureurs_formatted
    }
    

result = [ {"course": course, **v} for course, v in result.items()]
json.dump({"courses": result}, open("data/courses.json", "w"), indent=4, ensure_ascii=False)
