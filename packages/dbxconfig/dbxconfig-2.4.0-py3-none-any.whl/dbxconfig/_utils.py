import jinja2
from enum import Enum
import yaml
from pyspark.sql.types import StructType
from typing import Dict
import os


class JinjaVariables(Enum):
    DATABASE = "database"
    TABLE = "table"
    CHECKPOINT = "checkpoint"
    FILENAME_DATE_FORMAT = "filename_date_format"
    PATH_DATE_FORMAT = "path_date_format"
    CONTAINER = "container"


def render_jinja(data: str, replacements: Dict[JinjaVariables, str]):
    if data and isinstance(data, str):
        replace = {k.value: v for (k, v) in replacements.items()}
        skip = False
        for k, v in replace.items():
            if v is None and "{{" + k + "}}" in data.replace(" ", ""):
                skip = True
                break

        if not skip:
            template: jinja2.Template = jinja2.Template(data)
            data = template.render(replace)

    return data


def abs_config_path(root: str, path: str):
    if not os.path.isabs(path):
        path = os.path.join(root, path)
    return path


def load_schema(path: str):
    with open(path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    schema = StructType.fromJson(schema)

    return schema


def get_ddl(spark_schema: StructType, header: bool = True):
    if header:
        ddl = [f"{f.name} {f.dataType.simpleString()}" for f in spark_schema.fields]
    else:
        ddl = [
            f"_c{i} {f.dataType.simpleString()}"
            for i, f in enumerate(spark_schema.fields)
        ]

    return ddl


def get_html_table(data: dict):
    rows = []
    for k, v in data.items():
        if isinstance(v, dict):
            for ki, vi in v.items():
                row = f"<tr><td>{k}.{ki}</td><td>{vi}</td></tr>"
                rows.append(row)
        else:
            row = f"<tr><td>{k}</td><td>{v}</td></tr>"
            rows.append(row)

    html = "".join(rows)

    html = f"""
  <table>
    <tr><th>Name</th><th>Source</th><th>Destination</th></tr>
    {html}
  </table>
  """

    return html
