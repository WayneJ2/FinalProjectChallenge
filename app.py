from flask import Flask, render_template, current_app
import os
import pandas as pd
import joblib


# Flask Setup
app = Flask(__name__)

# Function to sample ten rows
def sample_rows(X_test, y_test):
    sample_X = X_test.sample(10)
    indices = sample_X.index
    return sample_X, y_test.loc[indices]

# Function to clean rendered table
def clean_columns(df):
    category_columns = ['category_entertainment',
       'category_food_dining', 'category_gas_transport',
       'category_grocery_net', 'category_grocery_pos',
       'category_health_fitness', 'category_home', 'category_kids_pets',
       'category_misc_net', 'category_misc_pos', 'category_personal_care',
       'category_shopping_net', 'category_shopping_pos', 'category_travel']

    gender_columns = ['gender_F', 'gender_M']

    week_columns = ['week_Friday', 'week_Monday', 'week_Saturday',
       'week_Sunday', 'week_Thursday', 'week_Tuesday', 'week_Wednesday']
    
    column_names = ["category", "gender", "week"]
    column_list_data = [category_columns, gender_columns, week_columns]
    
    for name, columns in zip(column_names, column_list_data):
        data = df[columns].apply(lambda x: df[columns].columns[x.argmax()], axis=1)
        df[name] = data.str.split("_", n=1, expand=True)[1]
        df.drop(columns, axis=1, inplace=True)
        
    df.rename({"amt": "Transaction Amount", "trans_hour": "Hour of Transaction", "age": "Age of Shopper",
           "category": "Category of Goods", "gender": "Gender of Shopper", "week": "Day of Week of Purchase"},
           axis=1, inplace=True)

    return df


# Function to 
def read_table():
    pass

X_test = pd.read_csv("X_test.csv", index_col = 0)
y_test = pd.read_csv("y_test.csv", index_col = 0)

model = joblib.load("model.pkl")

def get_results_table(X_sample, y_sample):
    predictions = model.predict(X_sample)
    prediction_series = pd.Series(predictions)
    y_sample["Machine Learning Fraud Prediction"] = prediction_series.values
    return y_sample

# Flask Render

@app.route("/")
def home():
    X_sample, y_sample = sample_rows(X_test, y_test)
    X_clean = clean_columns(X_sample.copy())
    X_test_table = X_clean.to_html(index = False)

    ten_row_list = ["" for _ in range(10)]
    empty_df = pd.DataFrame({"Actual Fraud Result": ten_row_list, "Machine Learning Fraud Prediction": ten_row_list})
    empty_table = empty_df.to_html(index=False, table_id="empty_table")

    results_df = get_results_table(X_sample, y_sample)
    results_df.rename({"is_fraud": "Actual Fraud Result"}, axis=1, inplace=True)
    results_df.replace({0: "Legitimate", 1: "Fraud"}, inplace = True)
    results_table = results_df.to_html(index=False, table_id="results_table")
    return render_template("index.html", table_data = X_test_table, empty_table = empty_table, results_table = results_table)

@app.route("/visuals.html")
def visuals():
    
    return render_template("visuals.html")



if __name__ == '__main__':
    app.run(debug=True)