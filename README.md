## Comparative Analysis of Ecommerce Platforms
This project compares pricing and discount trends for electronics like mobiles, headphones, and watches across Amazon, Flipkart, and Jiomart. Product data (name, price, discount) was collected using a Chrome extension and analyzed using Python (Pandas, NumPy).

An interactive dashboard built with Plotly Dash lets users filter by product type, brand, and model. It includes pages like an overview, raw data preview, price/discount comparisons, and platform-specific insights using line charts, bar graphs, and box plots.

The dashboard highlights variations in pricing strategies across platforms. Future upgrades may include real-time data, more product types, and predictive pricing analytics.
## Demo Video

<a href="https://youtu.be/jAeH3v5VpAs?si=4gaFDUcxDvfbNjvW" target="_blank">
  <img src="https://img.youtube.com/vi/jAeH3v5VpAs/maxresdefault.jpg" alt="Watch the video">
</a>


## Project Overview

This project analyzes and compares prices, discounts, ratings, and other details of electronic products from:

- **Amazon**
- **Flipkart**
- **Jiomart**

The goal is to help users identify where they can get the best deal on various mobile phones and accessories.

---

##  Project Structure

```
analysispart3/
├── app.py                      # Main dashboard app
├── pages/                     # Contains multipage content
│   ├── intro.py
│   ├── analytics.py
│   ├── dataset.py
│   ├── price-comparison.py
│   ├── discount-comparison.py
│   ├── flipkart_analytics.py
│   └── jiomart_analytics.py
├── assets/                    # Styling and custom layout
├── *.xlsx                     # Scraped product data
├── sweetviz_report.html       # Auto EDA report
└── your_report.html           # Final HTML report
```

---

##  Features

-  **Price Comparison** – Compare product prices across sites.
-  **Discount Insights** – Identify the highest discounts.
-  **Visual Charts** – Interactive Dash graphs for each platform.

---

##  How to Use

1. Clone the repository.
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```
4. Open your browser at:
   ```
   http://127.0.0.1:8050
   ```

---

## Preview


```[Dashboard_Ecommerce_Video](https://github.com/komalvinayak/Ecommerce_Analysis/blob/main/Ecommerce_Dashboard.mp4)``

---

<html>
<body>
<hr>

<h2>How It Works</h2>
<p>This dashboard works in a few simple steps:</p>
<h3>1. <strong>Data Collection</strong></h3>
<ul>
<li>
<p>Product data is scraped from <strong>Amazon</strong>, <strong>Flipkart</strong>, and <strong>Jiomart</strong>.</p>
</li>
<li>
<p>Collected details: Product Name, Price, Discount, Rating, Rating Count, and ASIN/URL.</p>
</li>

</ul>
<h3>2. <strong>Data Cleaning</strong></h3>
<ul>
<li>
<p>All collected data is cleaned using <strong>Pandas</strong>.</p>
</li>
<li>
<p>Null values, duplicates, and irrelevant fields are removed.</p>
</li>
</ul>
<h3>3. <strong>Data Analysis</strong></h3>
<ul>
<li>
<p>Analysis is done using:</p>
<ul>
<li>
<p><strong>Plotly Express</strong> for visual graphs.</p>
</li>
<li>
<p><strong>Pandas</strong> for statistical summaries.</p>
</li>
</ul>
</li>
</ul>
<h3>4. <strong>Interactive Dashboard</strong></h3>
<ul>
<li>
<p>Built using <strong>Plotly Dash</strong>.</p>
</li>
<li>
<p>Users can:</p>
<ul>
<li>
<p>Compare prices and discounts.</p>
</li>
<li>
<p>View platform-wise product insights.</p>
</li>
<li>
<p>Explore rating distributions.</p>
</li>
</ul>
</li>
</ul>
<hr>

<hr>
<h2> Data Collection</h2>
<h3> Sources:</h3>
<ul>
<li>
<p><strong>Amazon</strong> – via product ASIN scraping</p>
</li>
<li>
<p><strong>Flipkart</strong> – based on product titles and categories</p>
</li>
<li>
<p><strong>Jiomart</strong> – accessed using dynamic product URLs</p>
</li>
</ul>
<h3> Collected Fields:</h3>
for each platform
Field | Description
-- | --
Product Name | Name of the product
Price | Final listed price (₹)
Discount | % off on the MRP
Date | Date wise collection
URL/ASIN | Product Identifier


<h3>Output Format:</h3>
<ul>
<li>
<p>Data is saved in <code inline="">.xlsx</code> files per platform.</p>
</li>
<li>
<p>Combined files are used for dashboard analytics.</p>
</li>
</ul>

<hr>
<h3> Contact:</h3>


For questions or suggestions, feel free to open an issue or reach out on [[GitHub](https://github.com/komalvinayak)](https://github.com/komalvinayak).
<hr>
</body></html><!--EndFragment-->
</body>
</html>

