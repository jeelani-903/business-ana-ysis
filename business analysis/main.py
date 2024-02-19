import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('business data.csv')

# Assuming your dataset is stored in a DataFrame called df
# Convert 'Entry Date' column to datetime
df['Entry Date'] = pd.to_datetime(df['Entry Date'], format="%d-%m-%Y")

# Increase figure size
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot Quantity on the primary y-axis
df.groupby('city')['Quantity'].sum().plot(kind='bar', ax=ax1, color='blue', label='Total Quantity')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot Amount of Sales on the secondary y-axis
df.groupby('city')['Amount of Sales'].sum().plot(kind='bar', ax=ax2, color='maroon', label='Amount of Sales')

# Define colors for each group
group_colors = {'Apparel': 'orange', 'Home Textiles': 'green', 'Bedding': 'purple', 'Other': 'yellow'}

# Add another set of bars for total quantity sold for each 'Group'
ax3 = ax1.twinx()
df_group_quantity = df.groupby(['city', 'Group'])['Quantity'].sum().unstack()
df_group_quantity.plot(kind='bar', ax=ax3, stacked=True, color=[group_colors.get(group, 'gray') for group in df_group_quantity.columns])

# Add another set of bars for total sales by each company within a group
ax4 = ax1.twinx()
df_company_sales = df.groupby(['city', 'Group', 'Company'])['Amount of Sales'].sum().unstack()
df_company_sales.plot(kind='bar', ax=ax4, stacked=True, color='lightgray', width=0.3, position=1.2, edgecolor='black', legend=False)

# Set labels for the axes
ax1.set_ylabel('Quantity', color='blue')
ax2.set_ylabel('Amount of Sales', color='maroon')

# Set title
plt.title('Comparison of Quantity and Amount of Sales by City, Group, and Company')

# Add legend
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=df['Group'].nunique())

# Add text labels for each company at the side ends of the graph
for city in df['city'].unique():
    total_sales = df[df['city'] == city]['Amount of Sales'].sum()
    x_middle = df['city'].unique().tolist().index(city)
    x_offset = -0.35  # Adjust the offset to control the position of the labels
    for group in df['Group'].unique():
        for company in df[df['Group'] == group]['Company'].unique():
            sales_amount = df[(df['city'] == city) & (df['Group'] == group) & (df['Company'] == company)]['Amount of Sales'].sum()
            plt.text(x=x_middle + x_offset, y=sales_amount / 2, s=f"{company}\n{sales_amount}", ha='center', va='center', color='black')
            x_offset += 0.2  # Adjust the offset between companies

# Adjust layout to prevent clipping of labels
plt.tight_layout()

# Show the plot
plt.show()
