print("Starting the HealthCare Recommendation System...Loading the required libraries...")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from collections import Counter

from Components.Recommendation.doctorsRecommended import doctorsRecommended
from Components.Recommendation.orderByDistance import orderByDistance
from Models.Model import generateModel
from Models.Algorithms import algorithms

print("Loading the dataset...")

pd.set_option('display.max_colwidth', 100)

dis_sym_data = pd.read_csv("/datasets/Original_Dataset.csv")

# dis_sym_data.head()

dis_sym_data.shape

print("Data Preprocessing...This may take a while...")

columns_to_check = []
for col in dis_sym_data.columns:
    if col != 'Disease':
        columns_to_check.append(col)

symptoms = dis_sym_data.iloc[:, 1:].values.flatten()
symptoms = list(set(symptoms))

for symptom in symptoms:
    dis_sym_data[symptom] = dis_sym_data.iloc[:, 1:].apply(lambda row: int(symptom in row.values), axis=1)

dis_sym_data_v1 = dis_sym_data.drop(columns=columns_to_check)

dis_sym_data_v1 = dis_sym_data_v1.loc[:, dis_sym_data_v1.columns.notna()]

dis_sym_data_v1.shape

dis_sym_data_v1.columns = dis_sym_data_v1.columns.str.strip()

dis_sym_data_v1.columns

print("Label Encoding...")

var_mod = ['Disease']
le = LabelEncoder()
for i in var_mod:
    dis_sym_data_v1[i] = le.fit_transform(dis_sym_data_v1[i])

X = dis_sym_data_v1.drop(columns="Disease")
y = dis_sym_data_v1['Disease']


print("Training the models....Please wait...")
generateModel(X,y)
print("Models trained successfully!")

## Data Preprocessing for Doctor Recommendation
doc_data = pd.read_csv("/datasets/Doctor_Versus_Disease.csv",encoding='latin1', names=['Disease','Specialist'])
# doc_data.tail(5)

doc_data['Specialist'] = np.where((doc_data['Disease'] == 'Tuberculosis'),'Pulmonologist', doc_data['Specialist'])

# doc_data.tail(10)

des_data = pd.read_csv("/datasets/Disease_Description.csv")

# des_data.head()

doctors_info_df = pd.read_csv('/datasets/Doctors_info.csv')
# Sort the DataFrame by 'Specialization'
doctors_info_df = doctors_info_df.sort_values(by='Specialization')

# Reset index after sorting
doctors_info_df = doctors_info_df.reset_index(drop=True)


test_col = []
for col in dis_sym_data_v1.columns:
    if col != 'Disease':
        test_col.append(col)


print("\n--------------------------------------------------------------------------------------------------\n")

test_data = {}
symptoms = []
predicted = []
def test_input():
    symptoms.clear()
    predicted.clear()
    num_inputs = int(input("Enter the number of symptoms you have: "))
    for i in range(num_inputs):
        user_input = input("Enter Symptoms #{}: ".format(i+1))
        symptoms.append(user_input)
    print("Symptoms you have:", symptoms)
    for column in test_col:
        test_data[column] = 1 if column.lower() in map(str.lower, symptoms) else 0
        test_df = pd.DataFrame(test_data, index=[0])
    print("\n--------------------------------------------------------------------------------------------------\n")
    print("Predicting Disease based on 6 ML algorithms...")
    print("\n--------------------------------------------------------------------------------------------------\n")
    for model_name, values in algorithms.items():
        predict_disease = values["model"].predict(test_df)
        predict_disease = le.inverse_transform(predict_disease)
        predicted.extend(predict_disease)
    disease_counts = Counter(predicted)
    percentage_per_disease = {disease: (count / 6) * 100 for disease, count in disease_counts.items()}
    result_df = pd.DataFrame({"Disease": list(percentage_per_disease.keys()),
                               "Chances": list(percentage_per_disease.values())})
    result_df = result_df.merge(doc_data, on='Disease', how='left')
    result_df = result_df.merge(des_data, on='Disease', how='left')
    return result_df



def test_input_2():
    patientName= input("Enter your name: ")
    days_input = input("Enter the preferable days for visit separated by commas (e.g., Mon,Wed,Fri), or leave blank if not applicable: ")
    days = days_input.strip() if days_input else None

    doctorIDS = []  
    # Display recommended doctors for all predicted diseases
    for index, row in table.iterrows():
        detected_disease= row['Disease']
        detected_specialist = row['Specialist']
        recommended_doctors = doctorsRecommended(doctors_info_df,detected_specialist, days)
        if(recommended_doctors.empty):
            print("\nNo doctors found for", detected_disease, "with specialist", detected_specialist, "on the specified days and location.")
        else:
            print("\nRecommended doctors for", detected_disease, "with specialist", detected_specialist, ":")
            for index, row in recommended_doctors.iterrows():
                print(row['Doctor_Name'], "(", row['Specialization'], ")", " - ", row['Work_Location'])
                doctorIDS.append(row)
        print("\n--------------------------------------------------------------------------------------------------\n")
    print("Do you want to know the approximate distance of the recommended doctors from your location?")
    answer= input("Enter 'yes' or 'no': ")
    if answer.lower() == 'yes':
        patientCity = input("Enter your current residing city : ") 
        patientState = input("Enter your current residing state : ")
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("Sorted order of the recommended doctors (in terms of their distance) in ascending order:")
        print("\n--------------------------------------------------------------------------------------------------\n")
        doctorIDdf=pd.DataFrame(doctorIDS)
        sortedDoctors=orderByDistance(doctorIDdf,patientCity)
        print(sortedDoctors)
    else:
        print("Thank you for using the HealthCare Recommendation System!")


def register_doctor():
    doctor_id= input("Enter your doctor ID: ")
    doctor_name = input("Enter your name: ")
    specialization = input("Enter your specialization: ")
    work_location = input("Enter your work location: ")
    availability = input("Enter your availability days separated by commas (e.g., Mon,Wed,Fri): ")
    city = input("Enter your city: ")
    state = input("Enter your state: ")
    fee= input("Enter your consultation fee: ")
    contact= input("Enter your contact number: ")
    recommendation_percent = 30  # Set default recommendation percent
    new_doctor = pd.DataFrame({"Doctor_ID": [doctor_id],
                               "Doctor_Name": [doctor_name],
                               "Specialization": [specialization],
                               "Work_Location": [work_location],
                               "City": [city],
                               "State": [state],
                               "Availability": [availability],
                               "Fee": [fee],
                               "Recommendation(in %)": [recommendation_percent],
                               "Contact_Info": [contact]})
    doctors_info_df = pd.read_csv("/Datasets/Doctors_info.csv")
    doctors_info_df = pd.concat([doctors_info_df, new_doctor], ignore_index=True)
    doctors_info_df.to_csv("/Datasets/Doctors_info.csv", index=False)
    print("Doctor registration successful!")


while True:

    doctors_info_df = pd.read_csv('/datasets/Doctors_info.csv')
    # Sort the DataFrame by 'Specialization'
    doctors_info_df = doctors_info_df.sort_values(by='Specialization')
    print("\n--------------------------------------")
    print("    HealthCare Recommendation System")
    print("--------------------------------------")
    print("1. Login as a patient")
    print("2. Login as a doctor")
    print("3. Leave feedback")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        table = test_input()
        print(table)
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("Let's provide you with the best recommended doctors for the above probable diseases.....\n")
        print("--------------------------------------------------------------------------------------------------\n")
        test_input_2()

    elif choice == '2':
        print("\nDoctor Registration:")
        register_choice = input("Would you like to register yourself as a doctor? (yes/no): ")
        if register_choice.lower() == 'yes':
            register_doctor()

    elif choice == '3':
        print("Leave Feedback:")
        # Add feedback functionality here

    elif choice == '4':
        print("Exiting HealthCare Recommendation System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a valid option (1/2/3/4).")
