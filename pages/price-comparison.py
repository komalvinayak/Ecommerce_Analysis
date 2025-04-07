import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

# Registering the page in Dash with custom settings for URL, name, and order
dash.register_page(__name__, path='/price-comparison', name="Price Comparison 📈", order=3)

####################### LOAD DATASET #############################
# Loading multiple Excel files containing product price data from different companies
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

# Adding product category ('Type') and brand ('Company') labels to each dataset
df_vivo['Type'] = 'Mobile'
df_vivo['Company'] = 'Vivo'
df_boat_watch['Type'] = 'Watch'
df_boat_watch['Company'] = 'boAt Watch'
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

# Combining all individual dataframes into a single unified DataFrame for analysis
df = pd.concat([df_vivo, df_motorola, df_redmi, df_iphone13, df_iphone14, df_iphone15, df_boat, df_redmi_buds, df_realme_buds, df_boat_watch])

# Handling missing discount data in the 'Discount On Jiomart' column by filling NaNs with 0
df['Discount On Jiomart'] = df['Discount On Jiomart'].fillna(0)
df['Discount On Amazon'] = df['Discount On Amazon'].fillna(0)
df['Discount On Flipkart'] = df['Discount On Flipkart'].fillna(0)
####################### PRICE COMPARISON ##########################
# Function to create a price comparison plot for the selected product version
def create_price_comparison(selected_version):
    # Filter the DataFrame for the selected product version
    filtered_df = df.loc[df['Product Name'] == selected_version]

    # Line plot to compare prices across Amazon, Flipkart, and Jiomart over time
    fig_line = px.line(
        data_frame=filtered_df,
        x='Date',
        y=['Price On Amazon', 'Price On Flipkart', 'Price On Jiomart'],
        title=f'Price Comparison for {selected_version}',
        labels={'value': 'Price', 'variable': 'Platform'},  # Labels for better clarity
    )

    # Box plot to show price distribution across the three platforms
    fig_box = px.box(
        data_frame=filtered_df,
        y=['Price On Amazon', 'Price On Flipkart', 'Price On Jiomart'],
        title=f'Price Distribution for {selected_version}',
        points='outliers',  # Show outliers in the distribution
    )

    # Applying dark theme and centering titles for better visual consistency
    fig_line.update_layout(
        title_text=f'Price Comparison for {selected_version}',
        title_x=0.5,
        template='plotly_dark',
    )
    fig_box.update_layout(
        title_text=f'Price Distribution for {selected_version}',
        title_x=0.5,
        template='plotly_dark',
        xaxis_title="Platform Names",
        yaxis_title="Discount (%)",
    )

    # Customizing axes labels
    fig_line.update_xaxes(title_text='Date')
    fig_line.update_yaxes(title_text='Price (in Indian Rupees)')
    fig_box.update_yaxes(title_text='Price (in Indian Rupees)')

    return fig_line, fig_box  # Return both line and box plot figures

####################### WIDGETS ################################
# Define options for the 'Type' dropdown menu
types = ['Mobile', 'Headphones', 'Watch']

# Create dropdowns for type, company, and version selection
type_dd = dcc.Dropdown(id='type-dropdown', options=[{'label': t, 'value': t} for t in types], value='Mobile', clearable=False)
company_dd = dcc.Dropdown(id='company-dropdown-price')
version_dd = dcc.Dropdown(id='version-dropdown-price', style={'marginBottom': '10px'})

####################### PAGE LAYOUT #############################
# Defining the layout of the page, including dropdowns and graphs
layout = html.Div([
    html.H1("Price Comparison Across Different Platforms", style={'textAlign': 'center'}),

    # Dropdowns for selecting product type, company, and specific version
    html.P("Select Type:"),
    type_dd,  # Type Dropdown

    html.P("Select Company:"),
    company_dd,  # Company Dropdown

    html.P("Select Version:"),
    version_dd,  # Version Dropdown

    # Graphs for price comparison and distribution
    dcc.Graph(id='price-graph', style={'width': '100%'}),  # Line Plot for Price Comparison
    dcc.Graph(id='box-graph', style={'width': '100%'})  # Box Plot for Price Distribution
], className="p-4 m-2")

####################### CALLBACKS ################################
# Callback to update the company dropdown based on the selected type
@callback(
    Output('company-dropdown-price', 'options'),
    Input('type-dropdown', 'value')
)
def update_company_dropdown(selected_type):
    if selected_type is None:
        return []  # Return empty if no type is selected

    # Get unique company names based on selected type
    companies = df[df['Type'] == selected_type]['Company'].unique()
    return [{'label': c, 'value': c} for c in companies]

# Callback to update the version dropdown based on the selected company
@callback(
    Output('version-dropdown-price', 'options'),
    Input('company-dropdown-price', 'value')
)
def update_version_dropdown(selected_company):
    # Return an empty list if no company is selected
    if not selected_company:
        return []

    # Get unique product names for the selected company, dropping any NaN values
    versions = df[df['Company'] == selected_company]['Product Name'].dropna().unique()

    # Return the options in the required format
    return [{'label': v, 'value': v} for v in versions]

# Callback to update both the line and box plots based on the selected product version
@callback(
    [Output('price-graph', 'figure'), Output('box-graph', 'figure')],
    Input('version-dropdown-price', 'value')
)
def update_price_graph(selected_version):
    if selected_version is None:
        return {}, {}  # Return empty figures if no version is selected

    # Generate both line and box plot figures using the helper function
    fig_line, fig_box = create_price_comparison(selected_version)
    return fig_line, fig_box  # Return both figures
