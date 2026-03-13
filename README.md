# Car Prices Morocco 🚗🇲🇦

An end-to-end Machine Learning project designed to scrape, analyze, and predict used car prices in the Moroccan market. This project utilizes web scraping for data collection and a Flask web application for real-time price estimation.

---

## 📋 Table of Contents
* [About the Project](#about-the-project)
* [Project Architecture](#project-architecture)
* [Dataset](#dataset)
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)
* [Usage](#usage)

---

## 📖 About the Project
The goal of this project is to provide a tool for estimating the market value of used cars in Morocco. By scraping listings from popular platforms (like Avito), the system learns the relationship between car features—such as brand, model, year, fuel type, and mileage—and their selling price.

### Key Features
* **Data Scraping**: Automated scripts to gather car listings from Moroccan marketplaces.
* **Data Processing**: Jupyter notebooks for cleaning, handling missing values, and feature engineering.
* **Exploratory Data Analysis (EDA)**: Visual insights into market trends and price distributions.
* **Price Prediction**: Machine Learning models (including **CatBoost**) trained on local data for high accuracy.
* **Web Interface**: A Flask-based application where users can input car details to get instant price estimates.

---

## 🏗 Project Architecture
The repository is structured to handle the full data science lifecycle:

* **Scrape.py**: The entry point for data collection via web scraping.
* **EDA.ipynb**: Analysis of the Moroccan automotive market trends.
* **Processing.ipynb**: Preparing and cleaning raw data for the model.
* **model_test.ipynb**: Training, tuning, and evaluating model performance.
* **FlaskApp/**: Contains the web deployment files.
* **db.sqlite3**: Local database for storing processed records.

---

## 📊 Dataset
The repository includes several CSV files representing different stages of data preparation:
* **avito_data.csv**: The raw data extracted from the web.
* **avito_data_EDA.csv**: Refined data used for generating insights.
* **train_selected.csv / test_selected.csv**: The final feature sets used to train and validate the predictive model.

---

## 🛠 Technologies Used
* **Python**: Core logic and scripting.
* **Pandas & NumPy**: Data manipulation and numerical analysis.
* **BeautifulSoup & Requests**: Web scraping tools.
* **CatBoost**: Gradient boosting algorithm optimized for categorical features.
* **Flask**: Lightweight web framework for the prediction app.
* **Jupyter Notebook**: Interactive environment for experimentation.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher.
* `pip` package manager.

### Installation
1. **Clone the repository**:
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
2. **Install dependencies**:
```
pip install flask pandas numpy catboost beautifulsoup4 scikit-learn
```
### 💻 Usage
1. **Scraping Fresh Data**:
```
python Scrape.py
```
1. **Exploring and Training**:
```
jupyter notebook Processing.ipynb
```
1. **Launching the Web App**:
```
cd FlaskApp
python app.py
```
