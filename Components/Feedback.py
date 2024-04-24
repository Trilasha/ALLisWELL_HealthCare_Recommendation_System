import pandas as pd

def collect_feedback_and_update_recommendation(doctors_info_df, feedback_dict):
    print("Welcome to the feedback collection system.")
    print("Doctors and their IDs:")
    print(doctors_info_df)
    def calculate_new_recommendation_percentage(current_percentage, total_score, total_feedback):
        new_score = total_score + current_percentage
        new_percentage = (new_score / total_feedback*2)
        return round(new_percentage, 2)
    
    def collect_feedback(feedback_dict):
        patient_name = input("Enter your name: ")
        doctor_id = int(input("Enter the doctor's ID you want to rate: "))
        
        if (patient_name, doctor_id) in feedback_dict:
            print("You have already rated this doctor.")
            return None, None, None, feedback_dict
        
        feedback_score = int(input("Enter your feedback score (between 0 to 5): "))
        
        if feedback_score < 0 or feedback_score > 5:
            print("Feedback score should be between 0 and 5.")
            return None, None, None, feedback_dict
        
        feedback_dict[(patient_name, doctor_id)] = feedback_score
        
        return patient_name, doctor_id, feedback_score, feedback_dict


    patient_name, doctor_id, feedback_score, feedback_dict = collect_feedback(feedback_dict)

    if patient_name and doctor_id and feedback_score:
        if doctor_id in doctors_info_df['Doctor_ID'].values:
            total_feedback = len(feedback_dict)
            total_score = sum(feedback_dict.values())

            current_percentage = doctors_info_df.loc[doctors_info_df['Doctor_ID'] == doctor_id, 'UserRating'].values[0]
            new_percentage = calculate_new_recommendation_percentage(current_percentage, total_score, total_feedback)
            doctors_info_df.loc[doctors_info_df['Doctor_ID'] == doctor_id, 'UserRating'] = new_percentage
            print(f"Thank you, {patient_name}! Your feedback has been recorded.")
        else:
            print("Doctor ID not found.")
    else:
        print("Feedback collection cancelled.")

    return doctors_info_df, feedback_dict