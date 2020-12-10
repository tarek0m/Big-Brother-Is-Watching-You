import pandas
import os


def read_csv_files():
    path = os.chdir(r'out\logs')

    # get only the columns you want from the csv files

    result_lists = [pandas.read_csv(file_, usecols=['Start', 'End']).to_dict(orient='records') 
                    for file_ in os.listdir(path)]

    '''
    for list_ in result_lists:
        for dict_ in list_:
            for value in dict_.values():
                append(value)
    '''
    result_list = [value for list_ in result_lists for dict_ in list_ for value in dict_.values()]
    df = pandas.DataFrame(columns=["Start", "End"])

    for i in range(0, len(result_list), 2):
        df = df.append({"Start": result_list[i], "End": result_list[i+1]}, ignore_index= True)

    return df
