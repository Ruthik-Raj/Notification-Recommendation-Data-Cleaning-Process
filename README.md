# User Activity Analysis Project

## Project Overview

This project processes event data, which contains timestamped records of user interactions. The goal is to break down user activity into hourly intervals and summarize this data in an easy-to-read format. This enables analysis of user behavior by the hour of the day, such as when users are most active.

## Main Steps in the Project

### 1. Loading Input Data
The project starts by loading a CSV file that contains user interaction events. Each record includes the user’s ID, the timestamp (`DATE`), and the duration (`DURATION`) of the event in minutes.

### 2. Converting the Timestamp
The `DATE` column, which contains the timestamp of each event, is converted into a `datetime` format to make it easier to manipulate and perform time-based calculations.

### 3. Extracting the Date
A new column is created to extract just the date (without the time) from the timestamp. This allows for easier grouping of data on a per-day basis.

### 4. Tracking User Activity by Hour
For each event, the script calculates the start and end times based on the timestamp and duration. Then, it loops through each hour between the start and end times to track the user’s activity. Each hour that the user was active is logged.

### 5. Creating an Activity DataFrame
Once all hours of user activity are recorded, a new DataFrame is created. This DataFrame contains one record per user per hour that they were active.

### 6. Pivoting Data for Hourly Breakdown
The script pivots the data so that each row represents a user’s activity for a specific day. Each hour of the day (e.g., 12am, 1am, etc.) becomes a separate column, and if the user was active during that hour, a value of `1` is recorded; otherwise, `0` is recorded.

### 7. Renaming Hour Columns
The columns representing hours are renamed to more human-readable labels, such as "12am", "1am", "2am", etc. This makes it easier for users to interpret the data.

### 8. Flattening the Data
After pivoting the data, the MultiIndex (which was created for the user ID and date) is flattened into regular columns for easier analysis and use.

### 9. Saving the Final Output
The final DataFrame, which contains the hourly activity data, is saved as a new CSV file. This file can be used for further analysis, visualization, or reporting.

## Purpose and Use Cases

### Purpose
The main goal of this project is to track user activity on an hourly basis, providing insights into when users are most active or engaged.

### Use Cases
- **Behavioral Analysis**: Understanding when users are most likely to engage with notifications, messages, or other interactions.
- **Optimization of User Interactions**: Identifying peak hours for user activity, which can help optimize the timing of notifications or campaigns.
- **Reporting and Visualization**: The processed data can be used to create heatmaps or time-series graphs for easy visual interpretation of user activity patterns.

## Conclusion

This project provides a structured approach to analyzing user activity over time. By processing timestamped event data and breaking it down by the hour, the project enables insights into user behavior, which can be applied for better engagement strategies, operational optimizations, or in-depth data analysis.

## Files

- **Input Data**: A CSV file containing user event data with `USER_ID`, `DATE`, and `DURATION` columns.
- **Output Data**: A CSV file containing hourly user activity data with columns representing each hour of the day (e.g., `12am`, `1am`, etc.) and values indicating activity during those hours.

