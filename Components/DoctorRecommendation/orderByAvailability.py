import bisect

def orderByAvailability(doctors_info_df,detected_specialist, special_days=None):
    # Used searchsorted to find the range of indices
    left_index = doctors_info_df['Specialization'].searchsorted(detected_specialist, side='left')
    right_index = doctors_info_df['Specialization'].searchsorted(detected_specialist, side='right')
    relevant_doctors = doctors_info_df.iloc[left_index:right_index]

    if special_days:
        special_days_list = [day.strip() for day in special_days.split(',')]
        relevant_doctors = relevant_doctors[relevant_doctors['Availability'].apply(lambda x: any(day in x.split(',') for day in special_days_list))]

    return relevant_doctors