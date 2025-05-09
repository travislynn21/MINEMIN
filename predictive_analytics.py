import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class PredictiveAnalytics:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = RandomForestClassifier()

    def load_data(self):
        data = pd.read_csv(self.data_path)
        return data

    def train_model(self):
        data = self.load_data()
        X = data.drop(columns=['churn'])
        y = data['churn']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        return self.model

    def predict(self, user_data):
        return self.model.predict(user_data)
