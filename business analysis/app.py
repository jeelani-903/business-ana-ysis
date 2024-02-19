# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.graph_objects as go
import json

# Create a Flask web application
app = Flask(__name__, static_url_path='/static')

# Load your dataset (update the path to your CSV file)
csv_file_path = 'static/data/business_data.csv'
# Specify encoding and explicitly specify columns to read
df = pd.read_csv(csv_file_path, encoding='utf-8', usecols=['Entry_Date', 'city', 'Group', 'Company', 'Quantity', 'Amount of Sales', 'Grade', 'Quality'])

# Convert 'Entry Date' column to datetime
df['Entry_Date'] = pd.to_datetime(df['Entry_Date'], format="%d-%m-%Y")

# Define color mapping for Grades
grade_colors = {'A': 'darkgreen', 'B': 'lightorange', 'C': 'red'}

# Define the route for the home page
# Define the route for the home page
@app.route('/')
def index():
    # Group by city, group, and company
    grouped_df = df.groupby(['city', 'Group', 'Company']).agg({
        'Quantity': 'sum',
        'Amount of Sales': 'sum',
        'Grade': 'first',
        'Quality': 'first'
    }).reset_index()

    # Further aggregation by city and company
    aggregated_df = grouped_df.groupby(['city', 'Company']).agg({
        'Quantity': 'sum',
        'Amount of Sales': 'sum'
    }).reset_index()

    # Create a treemap with Plotly Express
    fig_treemap = go.Figure()

    for city in aggregated_df['city'].unique():
        df_city = aggregated_df[aggregated_df['city'] == city]
        color_map = df_city.set_index('Company')['Grade'].map(grade_colors)

        fig_treemap.add_trace(go.Treemap(
            labels=df_city['Company'],
            parents=[city] * len(df_city),
            values=df_city['Amount of Sales'],
            hoverinfo='label+value+percent parent',
            marker=dict(
                colors=color_map,
                colorbar=dict(
                    title='Grade',
                    tickvals=[0, 1, 2],
                    ticktext=['A', 'B', 'C'],
                ),
            ),
            name=city
        ))

    # Dropdown menu for selecting companies
    companies = grouped_df['Company'].unique().tolist()

    selected_company = request.args.get('company', default=companies[0], type=str)

    # Plot overall performance for each city
    fig_city_performance = go.Figure()

    for city in aggregated_df['city'].unique():
        df_city = aggregated_df[aggregated_df['city'] == city]
        fig_city_performance.add_trace(go.Bar(
            x=df_city['Company'],
            y=df_city['Amount of Sales'],
            name=city,
            marker_color=df_city['Grade'].map(grade_colors)
        ))

    # Update layout for city performance
    fig_city_performance.update_layout(
        barmode='group',
        xaxis_title='Company',
        yaxis_title='Total Sales',
        title=f'Overall Performance by City',
    )

    # Convert figures to JSON strings
    treemap_data = json.dumps(fig_treemap, cls=plotly.utils.PlotlyJSONEncoder)
    city_performance_data = json.dumps(fig_city_performance, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', treemap_data=treemap_data, companies=companies,
                           selected_company=selected_company, city_performance_data=city_performance_data)


# Define a route to fetch historical performance data for a selected company and year range
@app.route('/get_history')
def get_history():
    selected_company = request.args.get('company', type=str)
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    # Filter the dataframe based on the selected company and year range
    df_selected_company = df[df['Company'] == selected_company]
    df_selected_year_range = df_selected_company[df_selected_company['Entry_Date'].dt.year.between(start_year, end_year)]

    # Define color mapping for Grades
    grade_colors = {'A': 'darkgreen', 'B': 'lightorange', 'C': 'red'}

    # Plot historical performance for the selected company and year range
    fig_history = go.Figure()

    for city in df_selected_year_range['city'].unique():
        df_city = df_selected_year_range[df_selected_year_range['city'] == city]
        for col in ['Quantity', 'Amount of Sales', 'Grade', 'Quality']:
            grade = df_city["Grade"].values[0]
            text_label = (
                f'{selected_company} has produced a quantity of {df_city["Quantity"].values[0]}<br>'
                f'{selected_company} quality produced was {df_city["Quality"].values[0]}<br>'
                f'{selected_company} grade scores a grade of {grade}'
            )
            color = grade_colors.get(grade, 'gray')
            fig_history.add_trace(go.Scatter(
                x=df_city['Group'],
                y=df_city[col],
                mode='lines+markers',
                name=f'{city} - {col}',
                text=text_label,
                hoverinfo='text+name',
                line=dict(color=color)
            ))

    # Update layout for historical performance
    fig_history.update_layout(title=f'Historical Performance of {selected_company} ({start_year} - {end_year})',
                              xaxis_title='Group')

    # Convert figure to JSON string
    history_data = json.dumps(fig_history, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'history_data': history_data})

# Define a route for the favicon
@app.route('/favicon.ico')
def favicon():
    return "", 404

# Define the main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
