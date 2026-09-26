# Context
Greatglobe Logistics is a global supply chain company that manages the shipment of more than 500 products for 20-30 client companies across multiple domains. Each shipment may require compliance with international trade regulations, including import/export documentation, customs duties, and payment procedures. For logistics managers and supply chain teams, gathering accurate documentation and understanding payment obligations for each shipment is time-consuming and prone to errors. Automating this process using data and intelligent agents can greatly improve operational efficiency.

Currently, retrieving product details and corresponding trade compliance requirements is a manual, fragmented process:

Product information is stored in internal databases (Product_ID, category, cost, etc.).
Compliance information such as required import/export documents, duty payment methods, and obligations must be researched online, which is slow and inconsistent.
This makes it difficult for logistics teams to quickly verify shipments, especially when handling multiple clients across different countries.

# Objective
The goal of this project is to build an interactive logistics assistant that:

Retrieves product details from a SQL database based on a user-provided Product_ID.
Uses a web agent to fetch up-to-date import/export documents and payment methods for the product’s HS/HSN code, based on source and destination countries.
Presents the information in a structured format, highlighting both required documentation and any additional compliance information if available.

# Data Description
The database contains product-level information that includes:

**Product_ID** - Unique identifier for each product.
**Product_Name** - Name of the product.
**Category** - Broad classification of the product (e.g., Electronics, Textiles, Pharmaceuticals).
**HSN_Code** - Harmonized System of Nomenclature code for customs classification.