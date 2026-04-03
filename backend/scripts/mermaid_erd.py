import sys
from pathlib import Path
from sqlalchemy import MetaData

# backend/ as root so "app" can be imported
BACKEND_ROOT = Path(__file__).resolve().parent.parent  # backend/
REPO_ROOT = BACKEND_ROOT.parent                        # second_brain/
sys.path.append(str(BACKEND_ROOT))

from app.db.base import Base

import app.models.account
import app.models.category
import app.models.subcategory
import app.models.transaction
import app.models.user
import app.models.city
import app.models.store
import app.models.item


def sqlalchemy_to_mermaid(metadata: MetaData) -> str:
    lines: list[str] = ["erDiagram"]

    # Define entities (tables and their columns)
    for table in metadata.sorted_tables:
        lines.append(f"    {table.name} {{")
        for column in table.columns:
            col_type = type(column.type).__name__

            # Encode PK/FK info inside the type string to avoid Mermaid parse issues
            tags = []
            if column.primary_key:
                tags.append("PK")
            if column.foreign_keys:
                tags.append("FK")

            if tags:
                col_type_str = f"{col_type}_{'_'.join(tags)}"
            else:
                col_type_str = col_type

            # Mermaid ER syntax: <type> <name>
            lines.append(f"        {col_type_str} {column.name}")
        lines.append("    }\n")

    # Define relationships based on foreign keys
    for table in metadata.sorted_tables:
        for column in table.columns:
            for fk in column.foreign_keys:
                source = table.name
                target = fk.column.table.name
                # Simple 1-to-many notation
                lines.append(f"    {target} ||--o{{ {source} : has")

    return "\n".join(lines)


if __name__ == "__main__":
    mermaid = sqlalchemy_to_mermaid(Base.metadata)

    # docs/features/db under repo root (not under backend)
    output_dir = REPO_ROOT / "docs" / "features" / "mermaid"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "schema.mmd"
    output_file.write_text(mermaid, encoding="utf-8")

    print(f"Mermaid ERD saved to {output_file}")