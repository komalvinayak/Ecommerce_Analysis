import pandas as pd  # Import pandas for data manipulation and analysis
import dash  # Import Dash framework for building web applications
from dash import dcc, html, callback  # Import necessary Dash components
from dash.dependencies import Input, Output  # Import Input and Output for callbacks
import plotly.express as px  # Import Plotly Express for easy data visualization

# Initialize the Dash app and register the page
dash.register_page(__name__, path='/jiomart_analytics', name="Jiomart🛒", order=7)

# Load datasets from Excel files into DataFrames
df_vivo = pd.read_excel('analysispart3/vivo.xlsx')
df_motorola = pd.read_excel('analysispart3/moto.xlsx')
df_redmi = pd.read_excel('analysispart3/redmi.xlsx')
df_iphone13 = pd.read_excel('analysispart3/iphone13.xlsx')
df_iphone14 = pd.read_excel('analysispart3/iphone14.xlsx')
df_iphone15 = pd.read_excel('analysispart3/iphone15.xlsx')
df_boat = pd.read_excel('analysispart3/boat.xlsx')
df_redmi_buds = pd.read_excel('analysispart3/redmi_buds.xlsx')
df_realme_buds = pd.read_excel('analysispart3/realme_buds.xlsx')
df_boat_watch = pd.read_excel('analysispart3/boat_watch.xlsx')

# Add 'Type' and 'Company' columns to each dataframe for categorization
product_dfs = [df_vivo, df_motorola, df_redmi, df_iphone13, df_iphone14, df_iphone15, df_boat, df_redmi_buds, df_realme_buds, df_boat_watch]
product_info = [
    ('Mobile', 'Vivo'), ('Mobile', 'Motorola'), ('Mobile', 'Redmi'), 
    ('Mobile', 'iPhone'), ('Mobile', 'iPhone'), ('Mobile', 'iPhone'), 
    ('Headphones', 'boAt'), ('Headphones', 'Redmi Buds'),
    ('Headphones', 'Realme Buds'), ('Watch', 'boAt Watch')
]

# Assign Type and Company to each dataframe based on the product
for df, (ptype, company) in zip(product_dfs, product_info):
    df['Type'] = ptype
    df['Company'] = company

# Concatenate all dataframes into a single DataFrame
df = pd.concat(product_dfs)

# Fill NaN values in the 'Discount On Jiomart' column with 0
df['Discount On Jiomart'] = df['Discount On Jiomart'].fillna(0)

# Define functions for creating the required types of charts

def create_line_chart(df):
    line = px.line(df, x='Date', y='Price On Jiomart', title="Price Over Time")
    line.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_dark',  # Apply dark theme
    )
    return line

def create_histogram(df):
    hist = px.histogram(df, x='Price On Jiomart', title="Product Price Distribution")
    hist.update_layout(
        title_x=0.5,
        template='plotly_dark',
    )
    return hist

def create_box_plot(df):
    box = px.box(df, y='Price On Jiomart', title="Price Distribution")
    box.update_layout(
        title_x=0.5,
        template='plotly_dark',
    )
    return box

def create_rolling_plot(df):
    # Calculate 3-day rolling mean for product price
    df['jiomart_rolling_mean'] = df['Price On Jiomart'].rolling(window=3).mean()
    line = px.line(df, x='Date', y='jiomart_rolling_mean', title="3-Day Rolling Mean for Product Price")
    line.update_layout(
        title_x=0.5,
        template='plotly_dark',
    )
    return line

# Layout and widgets for the Dash app
types = ['Mobile', 'Headphones', 'Watch']  # Define product types for dropdown
layout = html.Div([
    html.H1("Jiomart Product Price & Discount Analysis", style={'textAlign': 'center'}),  # Title of the dashboard
    html.P("Select Type:"),
    dcc.Dropdown(
        id='type_dropdown-discount',  # Dropdown for product type selection
        options=[{'label': t, 'value': t} for t in types],
        value='Mobile',  # Default value
        clearable=False
    ),
    html.P("Select Company:"),
    dcc.Dropdown(id='company_dropdown-discount'),  # Dropdown for company selection
    html.P("Select Product Version:"),
    dcc.Dropdown(id='version_dropdown-discount', style={'marginBottom': '10px'}),  # Dropdown for product version selection

    # Graph containers
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        html.Div(dcc.Graph(id='line-chart-'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='histogram-'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='box-plot-'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='rolling-plot-'), style={'flex': '0 0 49%', 'margin': '0%'}),
    ])
], className="p-4 m-2")  # Main layout of the dashboard

# Callbacks for dropdown updates

@callback(
    Output('company_dropdown-discount', 'options'),  # Update options for company dropdown
    Input('type_dropdown-discount', 'value')  # Triggered by type dropdown
)
def update_company_dropdown(selected_type):
    # Get unique companies based on selected product type
    companies = df[df['Type'] == selected_type]['Company'].unique()
    return [{'label': c, 'value': c} for c in companies]  # Return updated options

@callback(
    Output('version_dropdown-discount', 'options'),  # Update options for version dropdown
    Input('company_dropdown-discount', 'value')  # Triggered by company dropdown
)
def update_version_dropdown(selected_company):
    if selected_company is None:
        return []  # Return empty if no company is selected

    # Get unique product versions for the selected company
    versions = df[df['Company'] == selected_company]['Product Name'].unique()
    return [{'label': v, 'value': v} for v in versions]

# Callback for updating selected graphs based on selected version
@callback(
    [
        Output('line-chart-', 'figure'),
        Output('histogram-', 'figure'),
        Output('box-plot-', 'figure'),
        Output('rolling-plot-', 'figure')
    ],
    Input('version_dropdown-discount', 'value')  # Triggered by version dropdown
)
def update_graphs(selected_version):
    # Filter dataframe based on selected version
    filtered_df = df[df['Product Name'] == selected_version]
    if filtered_df.empty:
        return [dash.no_update] * 4  # Return no update if no data available

    # Generate each graph with the filtered data
    return (
        create_line_chart(filtered_df),
        create_histogram(filtered_df),
        create_box_plot(filtered_df),
        create_rolling_plot(filtered_df)
    )
