
def doctorsRecommended(doctors_info_df,detected_specialist, special_days=None):
    relevant_doctors = doctors_info_df[doctors_info_df['Specialization'] == detected_specialist]
    # relevant_doctors_new.head()
    # print(relevant_doctors)
    if special_days:
        # Convert the input string of days into a list
        special_days_list = [day.strip() for day in special_days.split(',')]
        # Check if any of the days in the list is in the Availability column
        relevant_doctors = relevant_doctors[relevant_doctors['Availability'].apply(lambda x: any(day in x.split(',') for day in special_days_list))]

    return relevant_doctors
