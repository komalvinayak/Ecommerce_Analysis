import pandas as pd 
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the Dash app
dash.register_page(__name__, path='/flipkart_analytics', name="Flipkart🛒", order=6)

# Load datasets
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

# Add 'Type' and 'Company' columns to each dataframe
product_dfs = [df_vivo, df_motorola, df_redmi, df_iphone13, df_iphone14, df_iphone15, df_boat, df_redmi_buds, df_realme_buds, df_boat_watch]
product_info = [
    ('Mobile', 'Vivo'), ('Mobile', 'Motorola'), ('Mobile', 'Redmi'), ('Mobile', 'iPhone'),
    ('Mobile', 'iPhone'), ('Mobile', 'iPhone'), ('Headphones', 'boAt'), ('Headphones', 'Redmi Buds'),
    ('Headphones', 'Realme Buds'), ('Watch', 'boAt Watch')
]

for df, (ptype, company) in zip(product_dfs, product_info):
    df['Type'] = ptype
    df['Company'] = company

# Concatenate all dataframes
df = pd.concat(product_dfs)
df['Discount On Flipkart'] = df['Discount On Flipkart'].fillna(0)  # Ensure to fill missing values

# Define functions for creating each graph
def create_line_chart(df):
    line = px.line(df, x='Date', y='Price On Flipkart', title="Price Over Time")
    line.update_layout(title_x=0.5, template='plotly_dark')
    return line

def create_histogram(df):
    hist = px.histogram(df, x='Price On Flipkart', title="Distribution of Prices")
    hist.update_layout(title_x=0.5, template='plotly_dark')
    return hist

def create_box_plot(df):
    box = px.box(df, y='Price On Flipkart', title="Price Distribution")
    box.update_layout(title_x=0.5, template='plotly_dark')
    return box

def create_rolling_plot(df):
    df['flipkart_rolling_mean'] = df['Price On Flipkart'].rolling(window=3).mean()
    rol = px.line(df, x='Date', y='flipkart_rolling_mean', title="3-Day Rolling Mean of Product Price")
    rol.update_layout(title_x=0.5, template='plotly_dark')
    return rol

# Layout and widgets
types = ['Mobile', 'Headphones', 'Watch']
layout = html.Div([
    html.H1("Flipkart Product Price & Discount Analysis", style={'textAlign': 'center'}),
    html.P("Select Type:"),
    dcc.Dropdown(
        id='type-dropdow_discount', 
        options=[{'label': t, 'value': t} for t in types], 
        value='Mobile', 
        clearable=False
    ),
    html.P("Select Company:"),
    dcc.Dropdown(id='company-dropdow_discount'),
    html.P("Select Version:"),
    dcc.Dropdown(id='version-dropdow_discount', style={'marginBottom': '10px'}),

    # Graph containers organized into rows and columns
    html.Div(className="graph-container", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

    # Each graph in a 4x1 arrangement (removed the charts we don't need)
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        html.Div(dcc.Graph(id='linechart'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='histogram_'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='boxplot'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='rollingplot'), style={'flex': '0 0 49%', 'margin': '0%'}),  # Last graph takes full width
    ])
], className="p-4 m-2")

# Callbacks for dropdown updates
@callback(
    Output('company-dropdow_discount', 'options'),
    Input('type-dropdow_discount', 'value')
)
def update_company_dropdown(selected_type):
    companies = df[df['Type'] == selected_type]['Company'].unique()
    return [{'label': c, 'value': c} for c in companies]

@callback(
    Output('version-dropdow_discount', 'options'),
    Input('company-dropdow_discount', 'value')
)
def update_version_dropdown(selected_company):
    if selected_company is None:
        return []  # Return empty if no company is selected

    versions = df[df['Company'] == selected_company]['Product Name'].unique()
    return [{'label': v, 'value': v} for v in versions]

# Callback for updating all graphs based on selected version
@callback(
    [
        Output('linechart', 'figure'),
        Output('histogram_', 'figure'),
        Output('boxplot', 'figure'),
        Output('rollingplot', 'figure')
    ],
    Input('version-dropdow_discount', 'value')
)
def update_graphs(selected_version):
    if selected_version is None:
        return [{}] * 4  # Return empty figures if no product is selected

    # Filter data for the selected product version
    filtered_df = df[df['Product Name'] == selected_version]

    # Generate each chart
    fig_line = create_line_chart(filtered_df)
    fig_histogram = create_histogram(filtered_df)
    fig_box = create_box_plot(filtered_df)
    fig_rolling = create_rolling_plot(filtered_df)

    return fig_line, fig_histogram, fig_box, fig_rolling
