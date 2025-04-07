import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/analytics', name="Amazon🛒", order=5)

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
df_boat_watch= pd.read_excel('analysispart3/boat_watch.xlsx')

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
df['Discount On Jiomart'] = df['Discount On Jiomart'].fillna(0)

# Define functions for creating each graph
def create_line_chart(df):
    fig_line = px.line(df, x='Date', y='Price On Amazon', title="Product Price Over Time")
    fig_line.update_traces(line=dict(color='#ff5733'))
    fig_line.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_dark',
        showlegend=True
    )
    return fig_line

def create_histogram(df):
    fig_hist = px.histogram(df, x='Price On Amazon', title="Distribution of Product Prices")
    fig_hist.update_traces(marker=dict(color='#ff5733'))
    fig_hist.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_dark',
    )
    return fig_hist

def create_box_plot(df):
    fig_box = px.box(df, y='Price On Amazon', title="Price Distribution")
    fig_box.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_dark',
    )
    return fig_box

def create_rolling_plot(df):
    df['amazon_rolling_mean'] = df['Price On Amazon'].rolling(window=3).mean()
    fig_l = px.line(df, x='Date', y='amazon_rolling_mean', title="3-Day Rolling Mean of Price")
    fig_l.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_dark',
    )
    return fig_l

# Layout and widgets
types = ['Mobile', 'Headphones', 'Watch']
layout = html.Div([
    html.H1("Amazon Product Price & Discount Analysis", style={'textAlign': 'center'}),
    html.P("Select Type:"),
    dcc.Dropdown(
        id='type-dropdow-discount', 
        options=[{'label': t, 'value': t} for t in types], 
        value='Mobile', 
        clearable=False
    ),
    html.P("Select Company:"),
    dcc.Dropdown(id='company-dropdow-discount'),
    html.P("Select Version:"),
    dcc.Dropdown(id='version-dropdow-discount', style={'marginBottom': '10px'}),

    # Each graph in a 5x2 arrangement
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        html.Div(dcc.Graph(id='line-chart'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='histogram'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='box-plot'), style={'flex': '0 0 49%', 'margin': '0%'}),
        html.Div(dcc.Graph(id='rolling-plot'), style={'flex': '0 0 49%', 'margin': '0%'}),
    ])
], className="p-4 m-2")

# Callbacks for dropdown updates
@callback(
    Output('company-dropdow-discount', 'options'),
    Input('type-dropdow-discount', 'value')
)
def update_company_dropdown(selected_type):
    companies = df[df['Type'] == selected_type]['Company'].unique()
    return [{'label': c, 'value': c} for c in companies]

@callback(
    Output('version-dropdow-discount', 'options'),
    Input('company-dropdow-discount', 'value')
)
def update_version_dropdown(selected_company):
    if selected_company is None:
        return []

    versions = df[df['Company'] == selected_company]['Product Name'].unique()
    return [{'label': v, 'value': v} for v in versions]

# Callback for updating all graphs based on selected version
@callback(
    [
        Output('line-chart', 'figure'),
        Output('histogram', 'figure'),
        Output('box-plot', 'figure'),
        Output('rolling-plot', 'figure')
    ],
    Input('version-dropdow-discount', 'value')
)
def update_graphs(selected_version):
    if selected_version is None:
        return [{}] * 4

    filtered_df = df[df['Product Name'] == selected_version]

    fig_line = create_line_chart(filtered_df)
    fig_histogram = create_histogram(filtered_df)
    fig_box = create_box_plot(filtered_df)
    fig_rolling = create_rolling_plot(filtered_df)

    return fig_line, fig_histogram, fig_box, fig_rolling
