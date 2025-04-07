# Import necessary libraries for data handling, Dash components, and visualization
import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go

# Register this file as a page in the Dash app with the path '/dataset' and name "Dataset 📋"
dash.register_page(__name__, path='/dataset', name="Dataset 📋", order=2)

####################### LOAD DATASET #############################

# Load individual Excel files containing product data
df_vivo = pd.read_excel('analysispart3/vivo.xlsx')
df_motorola = pd.read_excel('analysispart3/moto.xlsx')
df_redmi = pd.read_excel('analysispart3/redmi.xlsx')
df_iphone13 = pd.read_excel('analysispart3/iphone13.xlsx')
df_iphone14 = pd.read_excel('analysispart3/iphone14.xlsx')
df_iphone15 = pd.read_excel('analysispart3/iphone15.xlsx')
df_redmi_buds = pd.read_excel('analysispart3/redmi_buds.xlsx') 
df_realme_buds = pd.read_excel('analysispart3/realme_buds.xlsx') 
df_boat_watch = pd.read_excel('analysispart3/boat_watch.xlsx')

# Combine all individual dataframes into a single dataframe for display
df = pd.concat([df_vivo, df_motorola, df_redmi, df_iphone13, df_iphone14, df_iphone15, df_redmi_buds, df_realme_buds, df_boat_watch])

# Convert 'Date' column to datetime format and then reformat as 'dd-mm-yyyy'
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

# Handle missing values in the 'Discount On Jiomart' column by filling them with 0
df['Discount On Jiomart'] = df['Discount On Jiomart'].fillna(0)
df['Discount On Amazon'] = df['Discount On Amazon'].fillna(0)
df['Discount On Flipkart'] = df['Discount On Flipkart'].fillna(0)

# Format the discount columns as strings with a '%' symbol
df['Discount On Amazon'] = (df['Discount On Amazon'].astype(int).astype(str) + '%')
df['Discount On Jiomart'] = (df['Discount On Jiomart'].astype(int).astype(str) + '%')
df['Discount On Flipkart'] = (df['Discount On Flipkart'].astype(int).astype(str) + '%')

####################### PAGE LAYOUT #############################

# Define the layout of the page, including a title and data table
layout = html.Div(children=[
    # Page title
    html.H1("Dataset Preview", style={'textAlign': 'center'}, className='app-header'),
    
    # Line break for spacing
    html.Br(),
    
    # Data table to display the dataset, with pagination set to 10 rows per page
    dash_table.DataTable(
        data=df.to_dict('records'),  # Convert dataframe to dictionary format for Dash DataTable
        page_size=10,  # Show 10 rows per page
        style_table={
            'height': '400px',  # Set table height
            'width': '100%',    # Set table width
            'overflowY': 'auto'  # Enable vertical scrolling
        },
        style_data={
            'height': 'auto',  # Auto-adjust row height
            'textAlign': 'center'  # Center-align text in cells
        }
    ),
], className="bg-dark text-dark p-4 m-2")  # Apply background, text color, padding, and margin styling
