#  Create a sample pandas data frame as described here: https://raw.githubusercontent.com/moralescastillo/code_sample/main/sample_data.py
print(df.head())

# separate dependent and independent variables
X=df[df.columns[1:].to_list()]  # Independent
y=df[[df.columns[0]]]  # dependent

# Split dataset into training set and test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# From the dependent variables, define what is going to be scaled and hot-encoded
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelBinarizer

column_tuples = [
    (['clicks'], StandardScaler()),
    (['platform'], LabelBinarizer()),
    (['costs'], StandardScaler()),
    (['views'], StandardScaler())
]

# Create a data frame mapper
from sklearn_pandas import DataFrameMapper

mapper = DataFrameMapper(column_tuples, df_out=True)

# Transform X_train according to X_train
X_train_processed = mapper.fit_transform(X_train)

# Transform X_test according to X_train
X_test_processed = mapper.transform(X_train)
