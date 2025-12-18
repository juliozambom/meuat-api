import os
import zipfile
import gdown
import geopandas as gpd
from app.database import engine
from sqlalchemy import inspect
from shapely.geometry import MultiPolygon, Polygon

def seed_db():
    if inspect(engine).has_table("farms"):
        print("Database is already populated, skiping seed script...")
        return
    
    file_id = "15ghpnwzdDhFqelouqvQwXlbzovtPhlFe"
    data_dir = "data"
    zip_path = os.path.join(data_dir, "areaimovel.zip")
    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(zip_path):
        print("Iniciando download dos dados dos polígonos das fazendas do estado de São Paulo.")
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, zip_path, quiet=False)

    print("Extraindo arquivos...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
    
    shp_files = [f for f in os.listdir(data_dir) if f.endswith('.shp')]
    if not shp_files:
        print("Erro: Nenhum .shp encontrado.")
        return
    
    shapefile_path = os.path.join(data_dir, shp_files[0])
    
    chunk_size = 10000

    total_records = len(gpd.read_file(shapefile_path, ignore_geometry=True, engine="pyogrio"))

    print(f"Total farm records to populate in DB: {total_records}")

    for start in range(0, total_records, chunk_size):
        print(f"Processing farm records {start} to {min(start + chunk_size, total_records)}...")
        
        gdf = gpd.read_file(shapefile_path, rows=slice(start, start + chunk_size))

        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs(epsg=4326)

        mode = "replace" if start == 0 else "append"

        gdf["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature 
            for feature in gdf["geometry"]
        ]
        
        gdf.to_postgis("farms", engine, if_exists=mode, index=False)
        
        del gdf
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()