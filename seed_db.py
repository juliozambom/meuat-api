import os
import geopandas as gpd
from app.database import engine
from sqlalchemy import inspect
from shapely.geometry import MultiPolygon, Polygon

def seed_db():
    if inspect(engine).has_table("farms"):
        print("Database is already populated, skiping seed script...")
        return

    shapefile_path = "data/AREA_IMOVEL_1.shp"

    print("Looking if Shapefile exists...")

    if not os.path.exists(shapefile_path):
        print(f"Error: {shapefile_path} not found!")
        return
    
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