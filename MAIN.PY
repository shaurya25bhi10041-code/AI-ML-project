# ==========================================
# HOUSE PRICE PREDICTION SYSTEM WITH LOGIN
# ==========================================

import pandas as pd
import time
import pickle
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ==========================================
# USER AUTHENTICATION SYSTEM
# ==========================================

def signup():
    username = input("Create Username: ")
    password = input("Create Password: ")

    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")

    print("✅ Signup successful! Please login.\n")

def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        with open("users.txt", "r") as f:
            users = f.readlines()

            for user in users:
                u, p = user.strip().split(",")
                if u == username and p == password:
                    print("✅ Login successful!\n")
                    return True

        print("❌ Invalid credentials!\n")
        return False

    except:
        print("No users found. Please signup first.\n")
        return False

# ==========================================
# DATA FUNCTIONS
# ==========================================

def load_data():
    return pd.read_csv("data.csv")

def show_data_info(data):
    print("\n📊 Dataset Info:")
    print(data.info())
    print("\nSummary:")
    print(data.describe())

# ==========================================
# MODEL FUNCTIONS
# ==========================================

def train_model(data):
    X = data[['area', 'bedrooms', 'bathrooms']]
    y = data['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    return r2_score(y_test, y_pred)

def save_model(model):
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def price_category(price):
    if price < 4000000:
        return "Low"
    elif price < 7000000:
        return "Medium"
    else:
        return "Luxury"

# SAVE prediction with timestamp
def save_prediction(area, bedrooms, bathrooms, price):
    with open("predictions.txt", "a") as f:
        f.write(f"{datetime.datetime.now()},{area},{bedrooms},{bathrooms},{price}\n")

# CLEAN FORMATTED HISTORY VIEW
def show_predictions():
    try:
        with open("predictions.txt", "r") as f:
            lines = f.readlines()

            print("\n📜 Last 5 Predictions:\n")

            if len(lines) == 0:
                print("No predictions yet.")
                return

            for line in lines[-5:]:
                parts = line.strip().split(",")

                # NEW FORMAT (with timestamp)
                if len(parts) == 5:
                    time_stamp, area, bedrooms, bathrooms, price = parts

                    print(f"🕒 Time: {time_stamp}")
                    print(f"🏠 Area: {area} sq ft")
                    print(f"🛏 Bedrooms: {bedrooms}")
                    print(f"🛁 Bathrooms: {bathrooms}")
                    print(f"💰 Price: ₹{price}")
                    print("-" * 40)

    except:
        print("No prediction history found.")

def clear_history():
    open("predictions.txt", "w").close()
    print("🧹 History cleared!")

# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("""
====================================
   HOUSE PRICE PREDICTION SYSTEM
====================================
""")

    # LOGIN SYSTEM
    while True:
        print("\n1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            if login():
                break
        elif choice == '2':
            signup()
        elif choice == '3':
            print("Exiting program...")
            return
        else:
            print("Invalid choice!")

    # LOAD DATA & TRAIN MODEL
    data = load_data()

    print("\nTraining model...")
    time.sleep(1)

    model, X_test, y_test = train_model(data)
    save_model(model)

    accuracy = evaluate_model(model, X_test, y_test)
    print(f"📊 Model Accuracy (R²): {round(accuracy, 2)}")

    # MAIN MENU
    while True:
        print("\n===== MENU =====")
        print("1. Predict Price")
        print("2. Show Dataset Info")
        print("3. Show Model Accuracy")
        print("4. View Prediction History")
        print("5. Clear Prediction History")
        print("6. Exit")

        choice = input("Enter your choice: ")

        # PREDICT
        if choice == '1':
            try:
                area = float(input("Enter area (sq ft): "))
                bedrooms = int(input("Enter bedrooms: "))
                bathrooms = int(input("Enter bathrooms: "))

                prediction = model.predict([[area, bedrooms, bathrooms]])
                price = int(prediction[0])

                print("\n" + "="*40)
                print("🏠 HOUSE PRICE RESULT")
                print("="*40)
                print(f"Area: {area}")
                print(f"Bedrooms: {bedrooms}")
                print(f"Bathrooms: {bathrooms}")
                print(f"Estimated Price: ₹{price}")
                print(f"Category: {price_category(price)}")
                print("="*40)

                save_prediction(area, bedrooms, bathrooms, price)

            except:
                print("❌ Invalid input! Try again.")

        elif choice == '2':
            show_data_info(data)

        elif choice == '3':
            print(f"📊 Model Accuracy: {round(accuracy, 2)}")

        elif choice == '4':
            show_predictions()

        elif choice == '5':
            clear_history()

        elif choice == '6':
            confirm = input("Are you sure you want to exit? (y/n): ")
            if confirm.lower() == 'y':
                print("👋 Exiting program...")
                break

        else:
            print("❌ Invalid choice!")

# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()