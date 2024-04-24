# ALLisWELL - Healthcare Recommendation System

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Directory Structure](#directory-structure)
4. [AI Integration](#ai-integration)
5. [Features](#features)
7. [Technological Stack](#technological-stack)
8. [Demo](#demo)

## Installation

### Cloning the Repository

To get started with ALLisWELL, you first need to clone the repository to your local machine. Open your terminal and execute the following command:

```bash
git clone https://github.com/Trilasha/ALLisWELL_HealthCare_Recommendation_System.git
```

### Setting up a Virtual Environment
Setting up a virtual environment is crucial to ensure a clean and isolated environment for running the ALLisWELL system. Follow these steps to set up a virtual environment:

1. Open your terminal and navigate to the cloned directory (ALLisWELL) using the cd command.

2. Execute the following command to create a new virtual environment in a specified path:
```
python -m venv /path/to/new/virtual/environment
```
Replace /path/to/new/virtual/environment with the desired path where you want to create the virtual environment.

3. Alternatively, if you want to create the virtual environment within your project directory with the name .venv, you can use:
```
python -m venv .venv
```


### Installing Dependencies
Once the virtual environment is activated, you can install the required dependencies using pip. Make sure you have pip installed. If not, you can install it using:
```
python -m pip install --upgrade pip
```
Then, use the following command to install the dependencies listed in the requirements.txt file:

```
pip install -r requirements.txt
```
For more information on setting up virtual environments,you may refer to the [official Python documentation.](https://docs.python.org/3/library/venv.html)

## Usage
1. **Activate the Virtual Environment**: Before running the system, ensure that the virtual environment is activated. Use the appropriate command based on your operating system:

    - **On Windows**
    ```
    .venv\Scripts\activate
    ```
    - **On macOS and Linux**
    ```
    source .venv/bin/activate
    ```
2. **Start the System**: Run the main script `Main.py` using Python:

   ```bash
   python Main.py
   ```
## Directory Structure
```
    ├── Components/
    │   ├── Recommendation/
    │   │   ├── doctorsRecommended.py
    │   │   ├── orderByAvailability.py
    │   │   └── orderByDistance.py
    │   └── diseasePrediction.py
    |
    ├── Datasets/
    │   ├── Disease_Prediction.csv
    │   ├── Doctor_Versus_Disease.csv
    │   ├── Doctors_info.csv
    │   └── Original_Dataset.csv
    |
    ├── Models/
    │   ├── Algorithms.py
    │   └── Model.py
    |
    ├── Main.py
    ├── README.md
    └── requirements.txt
```

## AI Integration 

This project explores the use of machine learning algorithms to predict diseases from symptoms.

### Algorithms Explored
- **Logistic Regression**
- **Decision Tree**
- **Random Forest**
- **SVM**
- **NaiveBayes**
- **K-Nearest Neighbors**

Utilizing the above-mentioned machine learning algorithms, the prediction accuracy has been rigorously evaluated and found to ebe over 90%. This high accuracy rate ensures reliable disease prediction, providing users with confidence in the system's recommendations. 

## Features
//

//

//

## Technological Stack 
- **pandas**
- **numpy**
- **matplotlib**
- **seaborn**
- **scikit-learn**
- **warnings**
- **collections**
- **requests**
- **geopy**
- **bisect**
- **CSV Files**
- **Git**
- **GitHub**
- **Virtual Environment (venv)**


## Demo
//

//

//