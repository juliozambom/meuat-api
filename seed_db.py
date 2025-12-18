import os
import geopandas as gpd
from app.database import engine

def seed_db():
    shapefile_path = "data/AREA_IMOVEL_1.shp"

    print("Looking if Shapefile exists...")

    if not os.path.exists(shapefile_path):
        print(f"Error: {shapefile_path} not found!")
        return

    print("Reading Shapefile...")

    gdf = gpd.read_file(shapefile_path)

    if gdf.crs != "EPSG:4326":
        print("Converting coordinates to EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)

    print(f"Uploading {len(gdf)} farms to the database")
    
    gdf.to_postgis("farms", engine, if_exists="replace", index=False)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()