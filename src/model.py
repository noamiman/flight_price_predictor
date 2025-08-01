from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import joblib


df = pd.read_csv('/Users/noamiman/PycharmProjects/flight_price_predictor/data/cleaned_data.csv')

destinations = ['LON', 'NYC', 'PAR', 'BER', 'AMS', 'BCN', 'ROM', 'ATH', 'BKK', 'DXB']
destination_map = {
    destination: i for i, destination in enumerate(destinations)
}
df['destination_encoded'] = df['destination'].map(destination_map)

X = df.drop(columns=['price', 'origin', 'destination'])
Y = df['price']
print(X.dtypes)

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

print("R² Score:", r2_score(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

#R² Score: 0.9370857336962288
#RMSE: 13.75077544430023

# Save the model as a .pkl file
feature_columns = X.columns.tolist()
joblib.dump((model, feature_columns), 'flight_price_model.pkl')