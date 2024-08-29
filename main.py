import pandas as pd

def read_data():
    import pandas as pd

    headers = ["FirstName", "LastName", "Company", "BirthDate", "Salary", "Address","Suburb","State","Post","Phone","Mobile","Email" ]
    df = pd.read_csv("member-data.csv", header=None, names=headers, delimiter = '|')
    
    return df

def transform_date(df):
    import pandas as pd
    
    def convert_date(date_int):

        date_str = str(int(date_int))

        # Handle different lengths
        if len(date_str) == 7:  # Case like 1062000
            date_str = '0' + date_str
        elif len(date_str) == 8:  # Case like 10062000
            date_str = date_str
        else: 
            date_str = '30082074'#empty string

        return f"{date_str[:2]}/{date_str[2:4]}/{date_str[4:]}"
    
    def SalaryBucket(df):
    
        if df['Salary'] <= 50000:
            return 'A'
        elif df['Salary'] <= 100000:
            return 'B'
        elif df['Salary'] > 100000:
            return 'C'
        else :
            return np.nan
        
    def calculate_age_from_dob(df: pd.DataFrame, dob_column: str) -> pd.DataFrame:
        """
        Calculate age from date of birth in a Pandas DataFrame.

        Parameters:
        df (pd.DataFrame): DataFrame containing the date of birth column
        dob_column (str): Name of the column with date of birth in the format 'YYYY-MM-DD'

        Returns:
        pd.DataFrame: DataFrame with an additional column 'Age' containing the calculated age
        """
        # Ensure the DOB column is in datetime format
        df['new_dob_column'] = pd.to_datetime(df[dob_column], format='%d/%m/%Y')

        # Calculate age
        today = pd.Timestamp.today()
        df['Age'] = today.year - df['new_dob_column'].dt.year
        df = df.drop(columns=['new_dob_column'])

        return df
    
    df['BirthDate'] = df['BirthDate'].fillna(0)
    df['BirthDate'] = df['BirthDate'].apply(convert_date) 
    df['SalaryBucket'] = df.apply(SalaryBucket, axis = 1)
    df['Salary'] = df['Salary'].apply(lambda x: ''.join(('$', format(int(x), ','))) if not '$' in str(x) else x)
    df['FirstName'] = df['FirstName'].map(lambda x: x.strip() if isinstance(x, str) else x)
    df['LastName'] = df['LastName'].map(lambda x: x.strip() if isinstance(x, str) else x)
    df['FullName'] = df[df.columns[:2]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
    df = df.drop(columns=['FirstName', 'LastName'])
    df = calculate_age_from_dob(df, 'BirthDate')
    
    return df

def load_data(df):
    df.to_json('member-data.json', orient = 'split', compression = 'infer')

def main():
    df = read_data()
    df = transform_date(df)
    load_data(df)
  
if __name__ == "__main__":
    main()
