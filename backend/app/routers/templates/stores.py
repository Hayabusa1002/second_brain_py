TEMPLATE_CSV = """name,type,address,website,subcategory_names
Exito,physical,Carrera 43A # 1 Sur-150,,Food|Groceries|Household
Carulla,physical,Calle 10 # 43E-135,,Food|Groceries
Spotify,subscription,,https://spotify.com,Music|Entertainment
Netflix,subscription,,https://netflix.com,Streaming|Entertainment
Steam,online,,https://store.steampowered.com,Games|Digital Products
"""


TEMPLATE_JSON = [
    {
        "name": "Exito",
        "type": "physical",
        "address": "Carrera 43A # 1 Sur-150",
        "website": None,
        "subcategories": ["Food", "Groceries", "Household"],
    },
    {
        "name": "Carulla",
        "type": "physical",
        "address": "Calle 10 # 43E-135",
        "website": None,
        "subcategories": ["Food", "Groceries"],
    },
    {
        "name": "Spotify",
        "type": "subscription",
        "address": None,
        "website": "https://spotify.com",
        "subcategories": ["Music", "Entertainment"],
    },
    {
        "name": "Netflix",
        "type": "subscription",
        "address": None,
        "website": "https://netflix.com",
        "subcategories": ["Streaming", "Entertainment"],
    },
    {
        "name": "Steam",
        "type": "online",
        "address": None,
        "website": "https://store.steampowered.com",
        "subcategories": ["Games", "Digital Products"],
    },
]


TEMPLATE_YAML = """- name: Exito
  type: physical
  address: Carrera 43A # 1 Sur-150
  website:
  subcategories:
    - Food
    - Groceries
    - Household

- name: Carulla
  type: physical
  address: Calle 10 # 43E-135
  website:
  subcategories:
    - Food
    - Groceries

- name: Spotify
  type: subscription
  address:
  website: https://spotify.com
  subcategories:
    - Music
    - Entertainment

- name: Netflix
  type: subscription
  address:
  website: https://netflix.com
  subcategories:
    - Streaming
    - Entertainment

- name: Steam
  type: online
  address:
  website: https://store.steampowered.com
  subcategories:
    - Games
    - Digital Products
"""