import pandas as pd
import json

# Load your cleaned SQL-ready CSV
df = pd.read_csv('data/table.csv')
df2 = pd.read_csv('data/locations_only.csv')

def df_to_geojson_with_filters(df,df2):
    features = []
    only_coord = []
    # Specify the columns you want to use as filters or display in popups
    filter_columns = [
        'internal_id', 'Site_Name', 'Extreme_Group', 'Extreme_Subgroup', 
        'Administrative Region', 'Province', 'Temperature (°C)', 'pH'
    ]
    df2 = df2.head(5000)

    for _, row in df.iterrows():
        # Clean the data: Convert NaNs to None (JSON null)
        prop_dict = {col: (row[col] if pd.notna(row[col]) else None) for col in filter_columns}
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['Longitude (°E)']), float(row['Latitude (°N)'])]
            }, "properties" : prop_dict
        }
        features.append(feature)
    for _,row in df2.iterrows():
        feature2 = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['Longitude (°E)']), float(row['Latitude (°N)'])]
            }
        }
        only_coord.append(feature2)


    return features, only_coord

feat, coord = df_to_geojson_with_filters(df,df2)
# Save to your project data folder
with open('data/sites.json', 'w') as f:
    json.dump(feat,f)
with open('data/lat_long.json', 'w') as f2:
    json.dump(coord, f2)