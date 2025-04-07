
# Import necessary modules from Dash and other libraries
from dash import Dash, html, dcc  
# Imports core Dash components: Dash app, HTML, and Dash Core Components (dcc)
import dash   
# Imports the dash library for additional Dash features 
import plotly.express as px
# Imports Plotly Express for data visualization
import pandas as pd
# Imports pandas for data handling and manipulation 
# External CSS files for styling 

external_css = [ 
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",  # Bootstrap CSS for layout and styling
    '/assets/style.css'  # Custom CSS file located in the 'assets' directory of the Dash app

] 
# Initialize the Dash app
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)
 
# the layout of the app
app.layout = html.Div([  # Main container Div for the layout
    html.Br(),
    html.P(
        'Comparative Analysis of E-Commerce Platforms',  
        className="text-dark text-center fw-bold fs-1"  # Bootstrap classes for dark text, centered, bold, and large font size
    ),
   
    # Div container for navigation links with margin and alignment
    html.Div(
        style={'margin': '1px', 'textAlign': 'center'},  # Styling for the container: margin and center alignment
        children=[
            # Create a button for each page, linking to different pages in the app
            html.A(
                page['name'],  # The displayed name of the page
                href=page["relative_path"],  # URL for the page
                className="btn btn-dark m-1 fs-6"  # Bootstrap classes for dark button
            )
            for page in dash.page_registry.values()  # Loops through registered pages to generate links
        ]
    ),
    
    dash.page_container  # Container that holds the content of each page dynamically
], className="col-12 mx-auto")  # Bootstrap classes for full width and centered layout


# Run the app
if __name__ == '__main__':
    app.run(debug=True)  

