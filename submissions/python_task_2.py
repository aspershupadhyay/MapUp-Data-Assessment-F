import pandas as pd
from scipy.spatial import distance_matrix





def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df = pd.DataFrame(distance_matrix(df.values, df.values), index=df.id_start, columns=df.id_end)
    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_data = []

    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end: 
                distance = df.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df
    


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    unique_reference_distances = df[df['id_start'] == reference_id]['distance'].unique()

    threshold_multiplier = 0.1
    lower_bound = unique_reference_distances.min() - threshold_multiplier * unique_reference_distances.min()
    upper_bound = unique_reference_distances.max() + threshold_multiplier * unique_reference_distances.max()

    filtered_df = df[(df['id_start'] != reference_id) & (df['distance'].between(lower_bound, upper_bound))]

    return filtered_df 

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    
    moto_rate = 0.8
    car_rate = 1.2 
    rv_rate = 1.5
    bus_rate = 2.2
    truck_rate = 3.6
    
    df['moto'] = df['distance'] * moto_rate
    df['car'] = df['distance'] * car_rate
    df['rv'] = df['distance'] * rv_rate 
    df['bus'] = df['distance'] * bus_rate
    df['truck'] = df['distance'] * truck_rate
    
    return df