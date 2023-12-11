import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot_table(values="car", index="id_1", columns= "id_2", fill_value=0)

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = df['car'].apply(lambda x: 'low' if x <= 15 else 'medium' if x <= 25 else 'high')
    car_type_count = df['car_type'].value_counts().to_dict()
    sorted_car_type_count = sorted(car_type_count.items())
    return dict(sorted_car_type_count)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    bus_indexes = df.index[df['bus'] > 2 * bus_mean].tolist()
    return list(bus_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df['truck'] = pd.to_numeric(df['truck'], errors='coerce')
    routes = df.groupby('route')['truck'].mean().loc[lambda x: x > 7].index.tolist()
    
    return list(sorted(routes))


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    for column in matrix:
    # Apply the logic to each value
        matrix[column] = matrix[column].apply(lambda x: x * 0.75 if x > 20 else x * 1.25)
        # Round the values to 1 decimal place
        matrix[column] = matrix[column].round(1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    DAYS_IN_WEEK = 7
    # Write your logic here
    # Calculate durations in seconds
    df['durations'] = (df['end'] - df['start']).dt.total_seconds()

    # Group by (id, id_2) and calculate min, max durations
    result = (df.groupby(['id', 'id_2'])['durations']
                .agg(['min', 'max'])
             )

    # Check validity based on defined constants and 7-day span
    result['Invalid_timestamps'] = ((result['min'] == 0) &
                       (result['max'] == 86400) &
                       (result['max'] - result['min'] == DAYS_IN_WEEK * 86400))

    # Set MultiIndex then drop columns
    result = (result[['Invalid_timestamps']]
                .reset_index()
                .set_index(['id', 'id_2']))
    return pd.Series(result['Invalid_timestamps'])