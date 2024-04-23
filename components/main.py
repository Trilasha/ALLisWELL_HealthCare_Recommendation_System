import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from collections import Counter

from Recommendation.doctorsRecommended import doctorsRecommended

pd.set_option('display.max_colwidth', 100)

dis_sym_data = pd.read_csv("/datasets/Original_Dataset.csv")

dis_sym_data.head()

dis_sym_data.shape

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

var_mod = ['Disease']
le = LabelEncoder()
for i in var_mod:
    dis_sym_data_v1[i] = le.fit_transform(dis_sym_data_v1[i])

X = dis_sym_data_v1.drop(columns="Disease")
y = dis_sym_data_v1['Disease']

print("Training the models...")

def class_algo(model,independent,dependent):
    model.fit(independent,dependent)
    pred = model.predict(independent)
    accuracy = metrics.accuracy_score(pred,dependent)
    # print(model_name,'Accuracy : %s' % '{0:.3%}'.format(accuracy))

algorithms = {'Logistic Regression':
              {"model": LogisticRegression()},

              'Decision Tree':
              {"model": tree.DecisionTreeClassifier()},

              'Random Forest':
              {"model": RandomForestClassifier()},

              'SVM':
              {"model": svm.SVC(probability=True)},

              'NaiveBayes' :
              {"model": GaussianNB()},

              'K-Nearest Neighbors' :
              {"model": KNeighborsClassifier()},
             }


for model_name, values in algorithms.items():
    class_algo(values["model"],X,y)


doc_data = pd.read_csv("/datasets/Doctor_Versus_Disease.csv",encoding='latin1', names=['Disease','Specialist'])

# doc_data.tail(5)

doc_data['Specialist'] = np.where((doc_data['Disease'] == 'Tuberculosis'),'Pulmonologist', doc_data['Specialist'])

# doc_data.tail(10)

des_data = pd.read_csv("/datasets/Disease_Description.csv")

# des_data.head()

doctors_info_df = pd.read_csv('/datasets/Doctors_info.csv')



test_col = []
for col in dis_sym_data_v1.columns:
    if col != 'Disease':
        test_col.append(col)


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
        test_data[column] = 1 if column in symptoms else 0
        test_df = pd.DataFrame(test_data, index=[0])
    print("Predicting Disease based on 6 ML algorithms...")
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

table=test_input()
print(table)

print("Let's provide you with the best recommended doctors for the above probable diseases\n")



def test_input():
    special_days_input = input("Enter the preferable days for visit separated by commas (e.g., Mon,Wed,Fri), or leave blank if not applicable: ")
    special_days = special_days_input.strip() if special_days_input else None

    # Display recommended doctors for all predicted diseases
    for index, row in table.iterrows():
        detected_disease= row['Disease']
        detected_specialist = row['Specialist']
        recommended_doctors = doctorsRecommended(doctors_info_df,detected_specialist, special_days)
        if(recommended_doctors.empty):
            print("\nNo doctors found for", detected_disease, "with specialist", detected_specialist, "on the specified days and location.")
        print("\nRecommended doctors for", detected_disease, "with specialist", detected_specialist, ":")
        print(recommended_doctors)

test_input()
