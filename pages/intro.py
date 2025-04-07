# Importing the main Dash module and HTML components
import dash
from dash import html

# Register this page as the main (or introductory) page of the app with path '/' and name "Introduction"
dash.register_page(__name__, path='/', name="Introduction", order=1)

# List of features that will be displayed on the page
features = [
    "Date",
    "Product Name",
    "Price On Amazon",
    "Price On Flipkart",
    "Price On Jiomart",
    "Discount On Amazon",
    "Discount On Flipkart",
    "Discount On Jiomart"
]

####################### PAGE LAYOUT #############################

# Define the layout of the page
layout = html.Div(children=[
    # Section for the project introduction
    html.Div(children=[
        # Heading for the introduction section
        html.H2("Project Introduction", style={'textAlign': 'center'}),
        
        # Paragraph describing the project's purpose and scope
        html.P(
            "The Comparative Analysis of E-commerce Platforms project focuses on analysing product price and discount variations across three major platforms: Amazon, Flipkart, and Jiomart. In the rapidly growing world of online shopping, understanding pricing trends and platform competitiveness is crucial for both consumers and businesses. By collecting and analyzing pricing and discount data of various electronic products from three major shopping platforms of past few months, this project aims to uncover insights into price fluctuations, platform-specific pricing strategies, and discount analysis for cost-saving.",
            style={'textAlign': 'justify'}
        ),
    ]),
    
    # Section for displaying the list of data features
    html.Div(children=[
        html.Br(),  # Line break for spacing
        html.H2("Features Included In Data", style={'textAlign': 'center'}),  # Heading for the features section
        
        # Unordered list displaying each feature from the 'features' list
        html.Ul(children=[html.Li(feature) for feature in features])
    ])
    
], className="bg-dark text-light p-4 m-2")  # Styling the main container with Bootstrap classes
