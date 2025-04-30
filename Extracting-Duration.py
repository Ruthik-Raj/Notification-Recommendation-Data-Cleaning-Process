import pandas as pd
import json
from datetime import datetime, timedelta

# Load data
file_path = #'Sample_file'
df = pd.read_csv(file_path)

option_map = {
    0: '0 - 30 mins',
    1: '1 hour',
    2: 'Until Tomorrow Morning',
    3: 'Until I turn it back on',
    4: 'Custom'
}

# Convert LOCAL_TIME to datetime for easier handling
df['LOCAL_TIME'] = pd.to_datetime(df['LOCAL_TIME'])


# Function to extract the option value from the EVENT_PARAMS column
# def extract_option_value(EVENT_PARAMS):
#     try:
#         params = json.loads(EVENT_PARAMS)
#         for param in params:
#             if param.get('key') == 'option':
#                 return param['value']['string_value']
#             elif param.get('key') == 'duration':
#                 return float(param['value']['double_value'])
#     except Exception:
#         return None
def extract_option_value(EVENT_PARAMS):
    try:
        params = json.loads(EVENT_PARAMS)  # Parse the JSON string into a list of dictionaries
        for param in params:
            if param.get('key') == 'option':
                return param['value']['string_value']  # Extract the 'string_value' for the 'option' key
            elif param.get('key') == 'duration':
                return float(param['value']['string_value'])  # Extract the 'string_value' for 'duration' and convert it to a float
    except Exception as e:
        print(f"Error extracting option value: {e}")
        return None


# Helper function to calculate the time difference (in minutes) between two times
def time_diff(start_time, end_time):
    return (end_time - start_time).total_seconds() / 60  # returns duration in minutes


# Initialize a list to store results
results = []

# Iterate over the events
for i in range(len(df) - 1):
    event = df.iloc[i]

    # Check if the next event exists before proceeding with further checks
    if i + 1 >= len(df):  # Avoid accessing out-of-bounds indices
        break

    # If the event is "wyze_Event_home_noti_option_clicked"
    if event['EVENT_NAME'] == 'wyze_Event_home_noti_option_clicked':

        # Case 1: If the next event is "wyze_Event_home_noti_on_clicked"
        if i + 1 < len(df) and df.iloc[i + 1]['EVENT_NAME'] == 'wyze_Event_home_noti_on_clicked':
            start_time = event['LOCAL_TIME']
            off_time = df.iloc[i + 1]['LOCAL_TIME']
            duration = time_diff(start_time, off_time)
            results.append({
                'USER_ID': event['USER_ID'],
                'DATE': event['LOCAL_TIME'],
                'DURATION': duration,

            })

        # Case 2: If the next event is "wyze_Event_home_noti_off_clicked"
        elif i + 1 < len(df) and df.iloc[i + 1]['EVENT_NAME'] == 'wyze_Event_home_noti_off_clicked':
            start_time = event['LOCAL_TIME']
            option_value = extract_option_value(event['EVENT_PARAMS'])
            if option_value == '0':
                off_time = start_time + timedelta(minutes=30)
            elif option_value == '1':
                off_time = start_time + timedelta(hours=1)
            elif option_value == '2':
                off_time = datetime(start_time.year, start_time.month, start_time.day) + timedelta(days=1)
            else:
                off_time = start_time  # Default to start time if no valid option
            duration = time_diff(start_time, off_time)
            results.append({
                'USER_ID': event['USER_ID'],
                'DATE': event['LOCAL_TIME'],
                'DURATION': duration,

            })

        # Case 3: If the next event is "wyze_Event_home_noti_custom_save" and next-next event is "wyze_Event_home_noti_off_clicked"
        # if i + 2 < len(df) and df.iloc[i + 1]['EVENT_NAME'] == 'wyze_Event_home_noti_custom_save' and df.iloc[i + 2]['EVENT_NAME'] == 'wyze_Event_home_noti_off_clicked':
        #     custom_save_time = df.iloc[i + 1]['LOCAL_TIME']
        #     option_value = extract_option_value(df.iloc[i + 1]['EVENT_PARAMS'])
        #     off_time = df.iloc[i + 2]['LOCAL_TIME']
        #     duration = time_diff(custom_save_time, off_time)
        #     results.append({
        #         'USER_ID': event['USER_ID'],
        #         'DATE': event['LOCAL_TIME'],
        #         'DURATION': duration,
        #         'OPTION_VALUE': option_value
        #     })
        if i + 2 < len(df) and df.iloc[i + 1]['EVENT_NAME'] == 'wyze_Event_home_noti_custom_save' and df.iloc[i + 2][
            'EVENT_NAME'] == 'wyze_Event_home_noti_off_clicked':
            custom_save_time = df.iloc[i + 1]['LOCAL_TIME']
            print("I am here")
            print(df.iloc[i + 1]['LOCAL_TIME'])
            # Extract the 'duration' from the EVENT_PARAMS of the custom save event
            duration_value = extract_option_value(df.iloc[i + 1]['EVENT_PARAMS'])
            print("Duration")
            print(duration_value)

            off_time = custom_save_time + timedelta(hours=duration_value)


            duration = time_diff(custom_save_time, off_time)
            results.append({
                'USER_ID': event['USER_ID'],
                'DATE': event['LOCAL_TIME'],
                'DURATION': duration,
            })
        # Case 4: If the next event is "wyze_Event_home_noti_custom_save" and next-next event is "wyze_Event_home_noti_on_clicked"
        if i + 2 < len(df) and df.iloc[i + 1]['EVENT_NAME'] == 'wyze_Event_home_noti_custom_save' and df.iloc[i + 2]['EVENT_NAME'] == 'wyze_Event_home_noti_on_clicked':
            custom_save_time = df.iloc[i + 1]['LOCAL_TIME']
            on_click_time = df.iloc[i + 2]['LOCAL_TIME']
            duration = time_diff(custom_save_time, on_click_time)
            results.append({
                'USER_ID': event['USER_ID'],
                'DATE': event['LOCAL_TIME'],
                'DURATION': duration,

            })

# Create a DataFrame with the results
result_df = pd.DataFrame(results)

# Save to CSV
result_df.to_csv('/Users/ruthik.nataraja/Desktop/newyyyy.csv', index=False)
