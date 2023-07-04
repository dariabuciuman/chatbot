import pandas as pd
import json

xlsx_file = "D:/_licenta/backend/helpers/output_1684945587.xlsx"
json_file = "D:/_licenta/backend/helpers/good_intents.json"


def xlsx_to_json(xlsx_file, json_file):
    df = pd.read_excel(xlsx_file)

    intents = {}
    category_set = set()
    for index, row in df.iterrows():
        text = str(row[0])
        category = str(row[1])

        category_set.add(category)
        print(category_set)

        if category in intents:
            intents[category]["patterns"].append(text)
        else:
            intents[category] = {
                "tag": category,
                "patterns": [text],
                "responses": category
            }

    final_intents = list(intents.values())

    data = {
        "intents": final_intents
    }

    json_data = json.dumps(data, indent=4)

    with open(json_file, 'w') as f:
        f.write(json_data)
    print(json_data)


xlsx_to_json(xlsx_file, json_file)
