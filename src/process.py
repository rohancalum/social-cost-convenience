import pandas as pd 
import geopandas as gpd
import cenpy as cen
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os.path
import pickle
from urllib.error import HTTPError
my_path = os.path.abspath(os.path.dirname(__file__))



def get_city_names(fname = os.path.join(my_path, "../data/raw/cities.csv")):
    df = pd.read_csv(fname)
    return list(df['city_name'].unique())
    

def get_county_names(city_name: str, 
                    fname = os.path.join(my_path, "../data/raw/cities.csv")):
    df = pd.read_csv(fname)
    return list(df['county_name'][df['city_name']==city_name])
    

def read_rac(fname = os.path.join(my_path, "../data/raw/rac_all.csv")):
    '''
    Reads Resident Area Characteristics file and returns pandas DataFrame
    
    '''
    df = pd.read_csv(fname, encoding="ISO-8859-1")
    
    return df


def get_county_rac(df: pd.DataFrame, city_name: str, year = 2013):
    '''
    Returns county specific RAC data for a given city and year.
    
    '''
    county_list = get_county_names(city_name)
    df_county = df[df['ctyname'].isin(county_list)]
    df_county_year = df_county[df_county['year']==year]     
    
    return df_county_year


def get_city_geodata(city_name = 'Seattle, WA', level = 'tract', year = 2017):
    '''
    Returns the geometry for a specific city and Census year (> 2013).
    Default is Seattle, WA.
    
    '''    
    try:
        print("Returning geodata...")
        df = cen.products.ACS(year).from_place(place = city_name, 
                             place_type = 'Incorporated Place', 
                             level = level, return_geometry = True)
        path = os.path.join(my_path, "../data/processed/")
        print("Saving geodata...")
        
        try:
            tmp = pickle.load(open(path+city_name[:-4]+'_'+str(year)+'_geodata.pkl', "rb"))
        
        except (OSError, IOError) as e:
            tmp = df
            pickle.dump(tmp, open(path+city_name[:-4]+'_'+str(year)+'_geodata.pkl', "wb"))
            
    except HTTPError as e: 
        print("Census API not cooperating at the moment...")
        print(e.reason)
        
    return df


def get_centroids(geodata: gpd.GeoDataFrame) -> pd.DataFrame:
    '''
    Obtain centroids from . 
    
    '''    
    centroid_pts = geodata['geometry'].centroid.to_crs({'init': 'epsg:4326'})
    lat = centroid_pts.map(lambda p: str(p.y))
    lon = centroid_pts.map(lambda p: str(p.x))
    tract = geodata['tract']
    
    centroids = pd.DataFrame(data = {'lat': lat, 'lon': lon, 'tract':tract})
    centroids['coord'] = centroids[['lat', 'lon']].apply(lambda x: ','.join(x),
             axis=1)
    
    return centroids, tract


def plot_centroids(geodata: pd.DataFrame, city_name: str) -> gpd.GeoDataFrame:
    '''
    Plots centroids for testing. 
    
    '''    
    #TODO: Fix this.
    
#    tracts = gpd.GeoDataFrame(geometry = geodata['geometry'].copy())
#    centroids =  gpd.points_from_xy(geodata['lon'].apply(float), geodata['lat'].apply(float))
#    geo_df = gpd.GeoDataFrame(geodata, geometry = centroids)
#    geo_df.crs = ({'init': 'epsg:4326'})
#    tracts.crs = ({'init': 'epsg:4326'})
#    fig, ax = plt.subplots(figsize = (10,10))
#    tracts.plot(ax = ax, color='white', edgecolor='black')
#    geo_df.plot(ax = ax, color = 'r')
#    ax.set_title(city_name)
    print("This is broken")
    return 0

def main(default: bool, plot_output: bool, level: str,  year: int):
    
    if default:
        # This corresponds to Seattle
        i = -3
        j = -2
    else:
        # All cities
        i = 0
        j = None
        
    # Get all RAC data
    df = read_rac()
    
    # Get city names
    city_names = get_city_names()
    total = len(city_names)
    count = 0
    for city in city_names[i:j]:
        # Get the RAC data for the counties that belong to that city
        print("Working on: ", city)
        county_df = get_county_rac(df, city_name=city)
        gd = get_city_geodata(city_name = city)
        if plot_output: 
            plot_centroids(gd, city)
        centroids, tracts = get_centroids(gd)
        county_df['tract'] = county_df['trct'].apply(lambda x: str(x)[5:])
        new_df = pd.merge(county_df, centroids, on = 'tract', how = 'inner')
        path = os.path.join(my_path, "../data/processed/")
        new_df.to_pickle(path+city[:-4]+'_'+str(year)+'_rac_all.pkl')
        count += 1
        print("Completed {}/{} cities.".format(count, total))

if __name__ == '__main__':
    main(default=False, plot_output = False, level = 'tract', year = 2017)