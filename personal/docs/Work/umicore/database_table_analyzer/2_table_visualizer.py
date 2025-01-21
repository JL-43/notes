from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from fuzzywuzzy import process

app = Flask(__name__)

# Define the file path
FILE_PATH = './files/source.tsv'

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]

    # Initialize lists to store the two types of data
    column_info_data = []
    sample_value_data = []

    # Headers for the two types of data
    column_info_headers = ["TableName", "ColumnName", "DataType", "MaxValue", "MinValue", "AvgValue", "CountValue", "DistinctCountValue", "MaxDecimalPoints", "MaxLength", "MinLength"]
    sample_value_headers = ["TableName", "ColumnName", "DataType", "SampleValue"]

    # Parse the lines
    current_section = None
    for line in lines:
        if line.startswith("TableName\tColumnName\tDataType\tMaxValue"):
            current_section = "column_info"
        elif line.startswith("TableName\tColumnName\tDataType\tSampleValue"):
            current_section = "sample_value"
        elif current_section == "column_info":
            column_info_data.append(line.split('\t'))
        elif current_section == "sample_value":
            sample_value_data.append(line.split('\t'))

    # Create DataFrames
    column_info_df = pd.DataFrame(column_info_data, columns=column_info_headers)
    sample_value_df = pd.DataFrame(sample_value_data, columns=sample_value_headers)

    # Filter valid table names
    def is_valid_table_name(table_name):
        return bool(re.match(r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$', table_name))

    valid_column_info_df = column_info_df[column_info_df['TableName'].apply(is_valid_table_name)]
    valid_sample_value_df = sample_value_df[sample_value_df['TableName'].apply(is_valid_table_name)]

    print(f"Debug: Loaded {len(valid_column_info_df)} valid column info entries and {len(valid_sample_value_df)} valid sample value entries")

    return valid_column_info_df, valid_sample_value_df

def create_visualizations_for_table(column_info_df, sample_value_df, table_name):
    output_dir = f"static/visualizations/{table_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    table_column_info_df = column_info_df[column_info_df['TableName'] == table_name]
    table_sample_value_df = sample_value_df[sample_value_df['TableName'] == table_name]
    
    if table_column_info_df.empty or table_sample_value_df.empty:
        print(f"Debug: No data available for table {table_name}")
        return None, None, None

    column_counts = table_column_info_df['ColumnName'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    column_counts.plot(kind='bar', ax=ax, title=f"Columns in {table_name}")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Count")
    plt.tight_layout()
    column_path = os.path.join(output_dir, "columns.png")
    plt.savefig(column_path)
    plt.close()

    sample_value_counts = table_sample_value_df['SampleValue'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    sample_value_counts.plot(kind='bar', ax=ax, title=f"Sample Value Distribution in {table_name}")
    ax.set_xlabel("Sample Values")
    ax.set_ylabel("Count")
    plt.tight_layout()
    sample_value_path = os.path.join(output_dir, "sample_values.png")
    plt.savefig(sample_value_path)
    plt.close()

    # Check if 'DataType' column exists before generating the data type distribution visualization
    if 'DataType' in table_column_info_df.columns:
        data_type_counts = table_column_info_df['DataType'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 8))
        data_type_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', title=f"Data Type Distribution in {table_name}")
        plt.tight_layout()
        data_type_path = os.path.join(output_dir, "data_types.png")
        plt.savefig(data_type_path)
        plt.close()
    else:
        data_type_path = None

    return column_path, sample_value_path, data_type_path

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tables')
def tables():
    # Load data
    if not os.path.exists(FILE_PATH):
        error_message = "File not found at ./files/source.tsv. Please ensure the file is placed in the correct directory."
        return render_template("tables.html", error=error_message)

    column_info_df, sample_value_df = load_data(FILE_PATH)
    print(f"Data loaded with {len(column_info_df)} valid column info entries and {len(sample_value_df)} valid sample value entries")

    # Identify tables with data
    tables_with_data = column_info_df['TableName'].unique()

    # Identify tables without data
    all_tables = set(tables_with_data).union(set(sample_value_df['TableName'].unique()))
    tables_no_data = set()
    for table in all_tables:
        table_data = column_info_df[column_info_df['TableName'] == table]
        if table_data.empty or table_data.iloc[:, 2:].apply(lambda x: x.isnull() | (x == 'NULL') | (x == '0') | (x == 0)).all().all():
            tables_no_data.add(table)

    tables_with_data = set(tables_with_data) - tables_no_data

    return render_template("tables.html", tables_with_data=tables_with_data, tables_no_data=tables_no_data)

@app.route('/table/<table_name>')
def table_view(table_name):
    # Load data
    column_info_df, sample_value_df = load_data(FILE_PATH)

    if table_name not in column_info_df['TableName'].unique():
        return redirect(url_for('tables'))

    # Filter table-specific data for display
    table_data = column_info_df[column_info_df['TableName'] == table_name]
    sample_data = sample_value_df[sample_value_df['TableName'] == table_name]

    if table_data.empty or table_data.iloc[:, 3:].apply(lambda x: x.isnull() | (x == 'NULL') | (x == '0') | (x == 0)).all().all():
        print(f"Debug: No data found for table {table_name}.")
        return redirect(url_for('tables'))

    # Generate visualizations for the table
    column_vis_path, sample_value_vis_path, type_vis_path = create_visualizations_for_table(column_info_df, sample_value_df, table_name)

    table_data = table_data.to_dict(orient="records")
    sample_data = sample_data.to_dict(orient="records")

    print(f"Debug: Data found for table {table_name}: {table_data}")

    return render_template("table.html", 
                           table_name=table_name, 
                           column_vis_path=column_vis_path, 
                           sample_value_vis_path=sample_value_vis_path, 
                           type_vis_path=type_vis_path, 
                           table_data=table_data,
                           sample_data=sample_data)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return "<h1>Error: No search query provided.</h1>"

    # Load data
    column_info_df, sample_value_df = load_data(FILE_PATH)
    df = pd.concat([column_info_df, sample_value_df]).drop_duplicates()

    # Perform fuzzy search on ColumnName
    column_names = df['ColumnName'].unique()
    matches = process.extract(query, column_names, limit=10)
    matched_columns = [match[0] for match in matches]

    # Filter results based on matched columns and deduplicate
    results = df[df['ColumnName'].isin(matched_columns)].drop_duplicates(subset=['TableName', 'ColumnName']).to_dict(orient='records')

    return render_template("search_results.html", query=query, results=results)

@app.route('/getting-started')
def getting_started():
    return render_template("getting_started.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)