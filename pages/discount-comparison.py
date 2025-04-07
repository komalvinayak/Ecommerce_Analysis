# Import required libraries
import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

# Register the page in the Dash app with a specific route and name
dash.register_page(__name__, path='/discount-comparison', name="Discount Comparison 💸", order=4)

####################### LOAD DATASET #############################
# Load each product's data from Excel files into separate DataFrames
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

# Add 'Type' and 'Company' columns to each DataFrame for categorization
df_vivo['Type'] = 'Mobile'
df_vivo['Company'] = 'Vivo'

df_motorola['Type'] = 'Mobile'
df_motorola['Company'] = 'Motorola'

df_redmi['Type'] = 'Mobile'
df_redmi['Company'] = 'Redmi'

df_iphone13['Type'] = 'Mobile'
df_iphone13['Company'] = 'iPhone'

df_iphone14['Type'] = 'Mobile'
df_iphone14['Company'] = 'iPhone'

df_iphone15['Type'] = 'Mobile'
df_iphone15['Company'] = 'iPhone'

df_boat['Type'] = 'Headphones'  
df_boat['Company'] = 'boAt'

df_redmi_buds['Type'] = 'Headphones'
df_redmi_buds['Company'] = 'Redmi Buds'

df_realme_buds['Type'] = 'Headphones'
df_realme_buds['Company'] = 'Realme Buds'

df_boat_watch['Type'] = 'Watch'
df_boat_watch['Company'] = 'boAt Watch'

# Combine all DataFrames into a single DataFrame
df = pd.concat([df_vivo, df_motorola, df_redmi, df_iphone13, df_iphone14, df_iphone15, 
                df_boat, df_redmi_buds, df_realme_buds, df_boat_watch])

# Fill missing values in the 'Discount On Jiomart' column with 0
df['Discount On Jiomart'] = df['Discount On Jiomart'].fillna(0)
df['Discount On Amazon'] = df['Discount On Amazon'].fillna(0)
df['Discount On Flipkart'] = df['Discount On Flipkart'].fillna(0)

####################### DISCOUNT COMPARISON ######################
# Function to create figures for discount comparison for a specific product version
def create_discount_comparison(selected_version):
    # Filter the DataFrame to only include data for the selected version
    filtered_df = df[df['Product Name'] == selected_version]

    # Create a bar chart for discount comparison over time across platforms
    fig_bar = px.bar(
        data_frame=filtered_df,
        x='Date',
        y=['Discount On Amazon', 'Discount On Flipkart', 'Discount On Jiomart'],
        title=f'Discount Comparison for {selected_version}'
    )

    # Create a box plot to show discount distribution across platforms
    fig_box = px.box(
        data_frame=filtered_df,
        y=['Discount On Amazon', 'Discount On Flipkart', 'Discount On Jiomart'],
        title=f'Discount Distribution for {selected_version}',
        points='outliers'  # Show outliers
    )

    # Apply a dark theme and center the title in both charts
    fig_bar.update_layout(
        title_text=f'Discount Distribution for {selected_version}',
        title_x=0.5,
        template='plotly_dark',
    )

    fig_box.update_layout(
        title_text=f'Discount Comparison for {selected_version}',
        title_x=0.5,
        template='plotly_dark',
        xaxis_title="Platform Names",  
        yaxis_title="Discount (%)", 
    )

    return fig_box, fig_bar  # Return both figures for display

####################### WIDGETS #################################
# Define available product types
types = ['Mobile', 'Headphones', 'Watch']

# Dropdown for selecting product type
type_dd = dcc.Dropdown(
    id='type-dropdown-discount', 
    options=[{'label': t, 'value': t} for t in types], 
    value='Mobile', 
    clearable=False
)

# Dropdowns for selecting company and version, initially empty
company_dd = dcc.Dropdown(id='company-dropdown-discount')
version_dd = dcc.Dropdown(id='version-dropdown-discount', style={'marginBottom': '10px'})

####################### PAGE LAYOUT ##############################
# Define layout structure with dropdowns and graphs
layout = html.Div([
    html.H1("Discount Comparison Across Different Platforms", style={'textAlign': 'center'}),
    html.P("Select Type:"),
    type_dd,  # Product Type Dropdown
    html.P("Select Company:"),
    company_dd,  # Company Dropdown
    html.P("Select Version:"),
    version_dd,  # Product Version Dropdown
    dcc.Graph(id='discount-graph', style={'width': '100%'}),  # Box plot graph
    dcc.Graph(id='bar-graph', style={'width': '100%'})  # Bar chart graph
], className="p-4 m-2")

####################### CALLBACKS ################################
# Update company dropdown options based on selected type
@callback(
    Output('company-dropdown-discount', 'options'),
    [Input('type-dropdown-discount', 'value')]
)
def update_company_dropdown(selected_type):
    # Get unique companies for the selected product type
    companies = df[df['Type'] == selected_type]['Company'].unique()
    return [{'label': c, 'value': c} for c in companies]

# Update version dropdown options based on selected company
@callback(
    Output('version-dropdown-discount', 'options'),
    [Input('company-dropdown-discount', 'value')]
)
def update_version_dropdown(selected_company):
    if selected_company is None:
        return []  # Return empty if no company is selected

    # Get unique product versions for the selected company
    versions = df[df['Company'] == selected_company]['Product Name'].unique()
    return [{'label': v, 'value': v} for v in versions]

# Update graphs based on selected version
@callback(
    [Output('discount-graph', 'figure'), Output('bar-graph', 'figure')],
    [Input('version-dropdown-discount', 'value')]
)
def update_discount_graph(selected_version):
    if selected_version is None:
        return {}, {}  # Return empty figures if no version is selected

    # Generate both figures using the selected version
    fig_box, fig_bar = create_discount_comparison(selected_version)
    return fig_bar, fig_box  # Return both figures
