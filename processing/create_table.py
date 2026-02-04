import pandas as pd
import sqlite3

def transform_csv_to_sql(file_path, table_name, id_prefix):
    # Load the CSV
    df = pd.read_excel(file_path, sheet_name = 'Extreme_database')

    # 1. Add an internal incremental ID
    # This ensures every site has a unique key for the WebGIS
    # 2. Drop columns that are 100% empty (cleaning metadata)
    df = df.dropna(axis=1, how='all')
    print(len(df))
    # 3. Drop rows that are missing critical information
    # NOTE: We drop rows only if they lack BOTH a name and coordinates.
    # If we dropped rows with ANY empty field, we would lose almost all data.

    df['Longitude (°E)'] = pd.to_numeric(df['Longitude (°E)'], errors='coerce')
    df['Latitude (°N)'] = pd.to_numeric(df['Latitude (°N)'], errors='coerce')

    df = df.dropna(subset=['Site_Name', 'Latitude (°N)', 'Longitude (°E)'], how='all')
    df.insert(0, 'internal_id', [f"{id_prefix}_{i+1:05d}" for i in range(len(df))])
    print(len(df))

    # 4. Generate SQL (using SQLite as an example)
    conn = sqlite3.connect('site_database.db')
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    

    # 5. subset table to lat_long
    geo_loca = df[['Latitude (°N)', 'Longitude (°E)']]
    geo_loca.to_csv('locations_only.csv', index = None)

    # Export cleaned CSV for manual inspection
    output_name = f"sql_ready_{table_name}.csv"
    df.to_csv(output_name, index=False)
    
    print(f"Table '{table_name}' created with {len(df)} rows.")
    conn.close()

# Run the transformation for both datasets
sql_obj = transform_csv_to_sql('data/ITALIAN_SITE_TABLE.xlsx', 'extreme_sites', 'EXT')
