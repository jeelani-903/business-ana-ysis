from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Load your dataset
df = pd.read_csv('business data.csv')  # Update with the actual path to your dataset

# Assuming your dataset is stored in a DataFrame called df
# Convert 'Entry Date' column to datetime
df['Entry Date'] = pd.to_datetime(df['Entry Date'], format="%d-%m-%Y")

# Group by city, group, and company
grouped_df = df.groupby(['city', 'Group', 'Company']).agg({'Quantity': 'sum', 'Amount of Sales': 'sum'}).reset_index()

# Further aggregation by city and company
aggregated_df = grouped_df.groupby(['city', 'Company']).agg({'Quantity': 'sum', 'Amount of Sales': 'sum'}).reset_index()

@app.route('/')
def index():
    # Create a treemap with Plotly Express
    fig_treemap = px.treemap(aggregated_df, path=['city', 'Company'], values='Amount of Sales',
                             color='Quantity', hover_data=['Amount of Sales'],
                             color_continuous_scale='Viridis', title='Sales by City and Company')

    # Dropdown menu for selecting companies
    companies = grouped_df['Company'].unique().tolist()
    selected_company = request.args.get('company', default=companies[0], type=str)

    # Convert figures to JSON strings
    treemap_data = fig_treemap.to_json()

    # Plot overall performance for each city
    fig_city_performance = px.bar(aggregated_df[aggregated_df['Company'] == selected_company],
                                  x='city', y='Amount of Sales', color='Company',
                                  title=f'Overall Performance by City - {selected_company}',
                                  labels={'Amount of Sales': 'Total Sales'})

    # Convert figure to JSON string
    city_performance_data = fig_city_performance.to_json()

    # Plot overall performance by considering sales and group by each individual company in each city
    fig_overall_company = px.bar(grouped_df, x='city', y='Amount of Sales', color='Company',
                                 title='Overall Performance by City (Sales and Group by Company)',
                                 labels={'Amount of Sales': 'Total Sales'})

    # Convert figure to JSON string
    overall_company_data = fig_overall_company.to_json()

    return render_template('index.html', treemap_data=treemap_data, companies=companies,
                           selected_company=selected_company, city_performance_data=city_performance_data,
                           overall_company_data=overall_company_data)

@app.route('/get_history')
def get_history():
    selected_company = request.args.get('company', type=str)
    
    # Plot historical performance for the selected company
    fig_history = go.Figure()

    for city in grouped_df['city'].unique():
        df_city = grouped_df[(grouped_df['city'] == city) & (grouped_df['Company'] == selected_company)]
        for col in df_city.columns[3:]:  # Exclude 'Entry Date', 'city', 'Group', and 'Company'
            fig_history.add_trace(go.Scatter(x=df_city['Group'], y=df_city[col],
                                             mode='lines+markers', name=f'{city} - {col}'))

    # Update layout for historical performance
    fig_history.update_layout(title=f'Historical Performance of {selected_company} (All Data Fields)',
                              xaxis_title='Group')

    # Convert figure to JSON string
    history_data = fig_history.to_json()

    return jsonify({'history_data': history_data})

if __name__ == '__main__':
    app.run(debug=True)
