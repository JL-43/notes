# JL's Database Analyzer

## Features
- Database table structure analysis
- Column information visualization including:
  - Data types
  - Value ranges (min, max, avg)
  - Count statistics
  - Sample data preview
- Interactive web interface
  - Search functionality
  - Data visualization through charts

## Setup & Installation
1. Clone the repository: ..
2. Create and activate a virtual environment:
  ```
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. Install dependencies:
  ```
  pip install -r requirements.txt
  ```

## Usage
1. Data Extraction:
   - Run `1_read_tables.sql` in your SQL Server environment
   - Save the output to `source.tsv`

2. Launch the application: 

    ```python 2_table_visualizer.py```

3. Access the web interface:
   - Open a browser and navigate to `http://localhost:5000`
   - Start exploring tables through the interface

## Development History
The project has evolved from its initial version to now include:
- Added data type information in SQL queries
- Enhanced visualization capabilities
- Improved table structure analysis

## Future Development
Next steps include:
- Adding data type information to the table visualizations
- Creating a new sample data table view
- Improving the UI/UX for better data presentation

## Dependencies
Main dependencies include:
- Flask
- Pandas
- Matplotlib
- FuzzyWuzzy

See `requirements.txt` for a complete list.