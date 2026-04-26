TEMPLATE_CSV = """name,state,country
Medellin,Antioquia,Colombia
Bogota,Cundinamarca,Colombia
Madrid,,Spain
Buenos Aires,,Argentina
"""


TEMPLATE_JSON = [
    {
        "name": "Medellin",
        "state": "Antioquia",
        "country": "Colombia",
    },
    {
        "name": "Bogota",
        "state": "Cundinamarca",
        "country": "Colombia",
    },
    {
        "name": "Madrid",
        "state": None,
        "country": "Spain",
    },
    {
        "name": "Buenos Aires",
        "state": None,
        "country": "Argentina",
    },
]


TEMPLATE_YAML = """- name: Medellin
  state: Antioquia
  country: Colombia

- name: Bogota
  state: Cundinamarca
  country: Colombia

- name: Madrid
  state:
  country: Spain

- name: Buenos Aires
  state:
  country: Argentina
"""