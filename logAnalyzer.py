import pandas as pd
import matplotlib.pyplot as plt

log_path = 'part2.log'

df_log = pd.read_csv(log_path, sep='\t', header=None)

# Define a regular expression pattern to extract the date and time
date_pattern = r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})'
component_pattern = r'combo\s(.*?)\('
content_pattern = r':(.*$)'

# Extract the date and time into a new column
df_log['Date_Time'] = df_log[0].str.extract(date_pattern)

# Extract the component from the 4th column (index 3)
df_log['Component'] = df_log[0].str.extract(component_pattern)

df_log['Content'] = df_log[0].str.extract(content_pattern)

# Get the top 3 components
top_components = df_log['Component'].value_counts().head(3).index.tolist()

# Convert the "Date_Time" column to a datetime object
df_log['Date_Time'] = pd.to_datetime(df_log['Date_Time'], format='%b %d %H:%M:%S')

# Extract the hour from the "Date_Time" column
df_log['Hour'] = df_log['Date_Time'].dt.hour

# Create a function to classify hours as working hours or after hours
def classify_hour(hour):
    if 9 <= hour < 17:
        return 'Working Hours'
    else:
        return 'After Hours'

# Apply the classification function to create a new column
df_log['Period'] = df_log['Hour'].apply(classify_hour)

# Filter the DataFrame to include only the top 3 components
df_filtered = df_log[df_log['Component'].isin(top_components)]

# Count the entries for each component during the two periods
component_counts = df_filtered.groupby(['Component', 'Period']).size().unstack(fill_value=0)

# Plot the results
ax = component_counts.plot(kind='bar', stacked=True)
plt.xlabel('Component')
plt.ylabel('Number of Entries')
plt.title('Usage of Top 3 Components during Working Hours and After Hours')
plt.xticks(rotation=0)
plt.legend(title='Period')
plt.show()



