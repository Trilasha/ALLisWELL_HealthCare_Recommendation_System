
def orderByRating(doctorID_df):
    doctorID_df = doctorID_df.sort_values(by='UserRating', ascending=False)
    return doctorID_df
