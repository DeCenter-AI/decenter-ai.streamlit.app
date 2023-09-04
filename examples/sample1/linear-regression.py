
import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split

def train_model(dataset,pretrained_model=None):
    df = pd.read_csv(dataset)

    y = df['per_capita_income_in_usd']
    X = df[['year']]

    print(X,y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = pretrained_model or LinearRegression()
    # model.fit(X_train, y_train)
    model.fit(X,y)
    return model



if __name__=="__main__":
    import joblib
    dataset="canada_per_capita_income.csv"
    # m1 = train_model(dataset)
    # joblib.dump(m1, 'test-model.sav')

    m2 = joblib.load('trained-model-5f6042ce-4af4-11ee-9feb-a6a3d6f9860d-2023-09-04 12_56_33.569479 0.018210s.sav')
    train_model(dataset,m2)
