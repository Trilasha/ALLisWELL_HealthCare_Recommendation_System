from collections import Counter
import pandas as pd
from Models.Algorithms import algorithms
import numpy as np


doc_data = pd.read_csv("./Datasets/Doctor_Versus_Disease.csv",encoding='latin1', names=['Disease','Specialist'])
doc_data['Specialist'] = np.where((doc_data['Disease'] == 'Tuberculosis'),'Pulmonologist', doc_data['Specialist'])
des_data = pd.read_csv("./Datasets/Disease_Description.csv")


def predictDisease(test_data, symptoms, predicted,le,test_col):
    symptoms.clear()
    predicted.clear()
    patientName= input("Enter your name: ")
    num_inputs = int(input("Enter the number of symptoms you have: "))
    for i in range(num_inputs):
        user_input = input("Enter Symptoms #{}: ".format(i+1))
        symptoms.append(user_input)
    print("Symptoms you have:", symptoms)
    for column in test_col:
        test_data[column] = 1 if column.lower() in map(str.lower, symptoms) else 0
        test_df = pd.DataFrame(test_data, index=[0])
    print("\n--------------------------------------------------------------------------------------------------\n")
    print("Predicting the probable diseases based on the symptoms you have...")
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