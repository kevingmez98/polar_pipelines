import json

from polar_library.engine.core import PolarDataProcessor
from polar_library.engine.core.dag_cleaner import merge_pipeline_clean

processor = PolarDataProcessor()

# Leer los archivos locales
with open("polar_library/dag/edges.json", "r", encoding="utf-8") as f:
    edges_json = json.load(f)
with open("polar_library/dag/nodes.json", "r", encoding="utf-8") as f:
    nodes_json = json.load(f)
with open("polar_library/dag/operations.json", "r", encoding="utf-8") as f:
    operations_json = json.load(f)

pipeline_limpio = merge_pipeline_clean(
    edges_json=edges_json, nodes_json=nodes_json, operations_json=operations_json
)

with open("clean_pipeline.json", "w") as f:
    json.dump(pipeline_limpio, f)

print("CARGANDO DATOS")

df = processor.io.read_csv("polar_library/data/Orders_Central.csv")
# df = processor.io.read_xlsx("polar_library/data/netflix_titles.xlsx")
print(df)

columna_a_limpiar = "Ship Mode"
columna_anio = "Ship Year"
columna_mes = "Ship Month"
columna_dia = "Ship Day"

df_limpio = processor.conversion.make_date(df, columna_dia, columna_mes, columna_anio, "Ship date")


# df_limpio = processor.text.left(df_limpio, columna_a_eliminar, 2, False, "Ship-left")
# df_limpio = processor.text.right(df_limpio, columna_a_eliminar, 2, False, "Ship-right")

print(df_limpio)
