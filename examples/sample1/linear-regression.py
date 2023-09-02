
import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split

def train_model(dataset):
    df = pd.read_csv(dataset)

    y = df['per_capita_income_in_usd']
    X = df[['year']]

    print(X,y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    # model.fit(X_train, y_train)
    model.fit(X,y)
    return model


if __name__=="__main__":
    dataset="canada_per_capita_income.csv"
    train_model(dataset)