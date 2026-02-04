import pandas as pd
import json

# Load your cleaned SQL-ready CSV
df = pd.read_csv('data/table.csv')

def df_to_geojson_with_filters(df):
    features = []
    # Specify the columns you want to use as filters or display in popups
    filter_columns = [
        'internal_id', 'Site_Name', 'Extreme_Group', 'Extreme_Subgroup', 
        'Administrative Region', 'Province', 'Temperature (°C)', 'pH'
    ]
    
    for _, row in df.iterrows():
        # Clean the data: Convert NaNs to None (JSON null)
        prop_dict = {col: (row[col] if pd.notna(row[col]) else None) for col in filter_columns}
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['Longitude (°E)']), float(row['Latitude (°N)'])]
            },
            "properties": prop_dict
        }
        features.append(feature)
    
    return {"type": "FeatureCollection", "features": features}

# Save to your project data folder
with open('data/sites.json', 'w') as f:
    json.dump(df_to_geojson_with_filters(df), f)