Folder structure:
data-portfolio/
├── databases/
│   └── ecommerce.db (we'll create this)
├── sql_queries/
│   ├── create_tables.sql
│   ├── sample_queries.sql
│   └── advanced_queries.sql
├── python_scripts/
│   ├── create_database.py
│   ├── analyze_data.py
│   └── visualizations.py
├── jupyter_notebooks/
│   └── ecommerce_analysis.ipynb
└── README.md

Database realtionships:
    create_tables.sql contains these relationships:
    customers (1) ←→ (many) orders (1) ←→ (many) order_items (many) ←→ (1) products

    Real-World Scenarios This Handles:
    One customer, multiple orders (common in e-commerce)
    One order, multiple products (shopping cart with multiple items)
    Price changes over time (unit_price preserves historical pricing)
    Customer analytics (track customer behavior over time)

    Business Questions That Can Be Answered:
    "What's our monthly revenue?" ← Needs orders + order_items
    "Who are our top customers?" ← Needs customers + orders + order_items
    "What products are most profitable?" ← Needs products + order_items
    "Where are our customers located?" ← Needs customers