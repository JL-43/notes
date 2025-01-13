from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from fuzzywuzzy import process

app = Flask(__name__)

# Load and clean data
def load_data(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    headers = ["TableName", "ColumnName", "SampleValue", "DataType"]
    data = [line.split('\t') for line in lines if not line.startswith("TableName")]

    # Ensure all rows have the same number of columns as the headers
    data = [row for row in data if len(row) == len(headers)]

    df = pd.DataFrame(data, columns=headers)

    # Filter valid table names
    def is_valid_table_name(table_name):
        return bool(re.match(r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$', table_name))

    valid_entries = df[df['TableName'].apply(is_valid_table_name)]
    return valid_entries



# Save visualizations for a specific table
def create_visualizations_for_table(df, table_name):
    output_dir = f"static/visualizations/{table_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    table_df = df[df['TableName'] == table_name]
    
    # Columns in the table
    column_counts = table_df['ColumnName'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    column_counts.plot(kind='bar', ax=ax, title=f"Columns in {table_name}")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Count")
    plt.tight_layout()
    column_path = os.path.join(output_dir, "columns.png")
    plt.savefig(column_path)
    plt.close()

    # Data types in the table
    data_type_counts = table_df['DataType'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    data_type_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', title=f"Data Type Distribution in {table_name}")
    plt.tight_layout()
    data_type_path = os.path.join(output_dir, "data_types.png")
    plt.savefig(data_type_path)
    plt.close()
    
    return column_path, data_type_path

@app.route('/')
def index():
    # Load data
    file_path = './files/pi_tables_read.rpt'
    if not os.path.exists(file_path):
        return f"<h1>Error: File not found at {file_path}</h1>"

    df = load_data(file_path).drop_duplicates()
    print(f"Data loaded with {len(df)} valid entries")

    tables = df['TableName'].unique()
    return render_template("index.html", tables=tables)

@app.route('/table/<table_name>')
def table_view(table_name):
    # Load data
    file_path = './files/pi_tables_read.rpt'
    df = load_data(file_path).drop_duplicates()

    if table_name not in df['TableName'].unique():
        return f"<h1>Error: Table {table_name} not found in data.</h1>"

    # Generate visualizations for the table
    column_vis_path, type_vis_path = create_visualizations_for_table(df, table_name)

    # Filter table-specific data for display
    table_data = df[df['TableName'] == table_name].to_dict(orient="records")
    
    # Debug: Print table data structure
    # print(f"Table data for {table_name}:")
    # print(table_data)

    return render_template("table.html", 
                           table_name=table_name, 
                           column_vis_path=column_vis_path, 
                           type_vis_path=type_vis_path, 
                           table_data=table_data)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return "<h1>Error: No search query provided.</h1>"

    # Load data
    file_path = './files/pi_tables_read.rpt'
    df = load_data(file_path).drop_duplicates()

    # Perform fuzzy search on ColumnName
    column_names = df['ColumnName'].unique()
    matches = process.extract(query, column_names, limit=10)
    matched_columns = [match[0] for match in matches]

    # Filter results based on matched columns and deduplicate
    results = df[df['ColumnName'].isin(matched_columns)].drop_duplicates(subset=['TableName', 'ColumnName']).to_dict(orient='records')

    return render_template("search_results.html", query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
