
def orderByRating(doctor_info_df,doctorID_df):
    doctorID_df=doctor_info_df[doctor_info_df['Doctor_ID'].isin(doctorID_df[0].values)]
    #sort the dataframe by UserRating
    doctorID_df=doctorID_df.sort_values(by='UserRating',ascending=False)
    return doctorID_df