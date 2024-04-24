print("Starting the HealthCare Recommendation System...")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

print("Loading the required libraries...")
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from collections import Counter

print("Importing the required components...")
from Components.DoctorRecommendation.orderByAvailability import orderByAvailability
from Components.DoctorRecommendation.orderByDistance import orderByDistance
from Components.DoctorRecommendation.orderByRating import orderByRating
from Components.predictDisease import predictDisease
from Components.Feedback import collect_feedback_and_update_recommendation
from Models.Model import generateModel
from Models.Algorithms import algorithms



print("Loading the dataset...")
pd.set_option('display.max_colwidth', 100)
dis_sym_data = pd.read_csv("./Datasets/Original_Dataset.csv")

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



doctors_info_df = pd.read_csv('./Datasets/Doctors_info.csv')
#dataframe sorted by Specialization
doctors_info_df = doctors_info_df.sort_values(by='Specialization')
doctors_info_df = doctors_info_df.reset_index(drop=True)


test_col = []
for col in dis_sym_data_v1.columns:
    if col != 'Disease':
        test_col.append(col)


test_data = {}
symptoms = []
predicted = []
feedback_dict = {}

def recommendDoctors():
    days_input = input("Enter the specific days when you want to visit a doctor (separated by commas e.g., Mon,Wed,Fri), or leave blank if not applicable: ")
    days = days_input.strip() if days_input else None

    doctorIDS = []  
    # to display recommended doctors for all predicted diseases
    for index, row in table.iterrows():
        detected_disease= row['Disease']
        detected_specialist = row['Specialist']
        recommended_doctors = orderByAvailability(doctors_info_df,detected_specialist, days)
        if(recommended_doctors.empty):
            print("\nNo doctors found for", detected_disease, "with specialization as - ", detected_specialist, "on the specified days and location.")
        else:
            print("\nRecommended doctors for", detected_disease, "with specialization as - ", detected_specialist, ":")
            print(recommended_doctors)
            doctorIDS.extend(recommended_doctors['Doctor_ID'].values)
        print("\n--------------------------------------------------------------------------------------------------\n")
    print("Do you want to reorder the recommended doctors by the user ratings?")
    take_input= input("Enter 'yes' or 'no': ")
    if take_input.lower() == 'yes':
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("Sorted order of the recommended doctors (in terms of their user ratings) in descending order:")
        print("\n--------------------------------------------------------------------------------------------------\n")
        doctorID_df=pd.DataFrame(doctorIDS)
        sortedDoctorsByRating=orderByRating(doctors_info_df,doctorID_df)
        print(sortedDoctorsByRating)
    print("Do you want to know the approximate distance of the recommended doctors from your location?")
    answer= input("Enter 'yes' or 'no': ")
    if answer.lower() == 'yes':
        patientCity = input("Enter your current residing city : ") 
        patientState = input("Enter your current residing state : ")
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("Sorted order of the recommended doctors (in terms of their distance) in ascending order:")
        print("\n--------------------------------------------------------------------------------------------------\n")
        sortedDoctors=orderByDistance(doctors_info_df,doctorID_df,patientCity)
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
    recommendation_percent = 3
    new_doctor = pd.DataFrame({"Doctor_ID": [doctor_id],
                               "Doctor_Name": [doctor_name],
                               "Specialization": [specialization],
                               "Work_Location": [work_location],
                               "City": [city],
                               "State": [state],
                               "Availability": [availability],
                               "Fee": [fee],
                               "UserRating": [recommendation_percent],
                               "Contact_Info": [contact]})
    doctors_info_df = pd.read_csv("./Datasets/Doctors_info.csv")
    doctors_info_df = pd.concat([doctors_info_df, new_doctor], ignore_index=True)
    doctors_info_df.to_csv("./Datasets/Doctors_info.csv", index=False)
    print("Doctor registration successful!")


while True:
    doctors_info_df=pd.read_csv('./Datasets/Doctors_info.csv')
    print("\n---------------------------------------------------------------------------------")
    print("               Welcome to ALLisWELL - HealthCare Recommendation System               ")
    print("-----------------------------------------------------------------------------------\n")
    print("1. Login as a patient")
    print("2. Login as a doctor")
    print("3. Rate a doctor and provide feedback")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        table = predictDisease(test_data,symptoms,predicted,le,test_col)
        print(table)
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("Let's provide you with the best recommended doctors for the above probable diseases.....\n")
        print("--------------------------------------------------------------------------------------------------\n")
        recommendDoctors()

    elif choice == '2':
        print("\n------------ Doctor Registration ----------------:")
        register_choice = input("Would you like to register yourself as a doctor? (yes/no): ")
        if register_choice.lower() == 'yes':
            register_doctor()

    elif choice == '3':
        print("-------------- Leave a Feedback --------------------")
        doctors_info_df, feedback_dict = collect_feedback_and_update_recommendation(doctors_info_df, feedback_dict)

    elif choice == '4':
        print("Exiting ALLisWELL HealthCare Recommendation System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a valid option (1/2/3/4).")