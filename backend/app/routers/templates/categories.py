TEMPLATE_CSV = """name,type,subcategory_names
Job,income,Salary | Holiday Pay
Freelance,income,Projects | Tips | Bonus
"""

TEMPLATE_JSON = [
    {
        "name": "Job",
        "type": "income",
        "subcategories": [
            {"name": "Salary"},
            {"name": "Holiday Pay"},
        ],
    },
]

TEMPLATE_YAML = """- name: Job
  type: income
  subcategories:
    - name: Salary
    - name: Holiday Pay
"""