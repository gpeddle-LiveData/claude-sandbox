#!/usr/bin/env python3
"""CSV Sales Data Processor

Reads sales data and generates a summary report.
"""

import csv
from collections import defaultdict
from pathlib import Path


def process_sales_data(csv_path: str, output_path: str) -> None:
    """Process sales data and generate summary report.

    Args:
        csv_path: Path to input CSV file
        output_path: Path to output summary file
    """
    # Read and process data
    revenue_by_product = defaultdict(float)
    quantity_by_product = defaultdict(int)

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row['product']
            quantity = int(row['quantity'])
            price = float(row['price'])
            revenue = quantity * price

            revenue_by_product[product] += revenue
            quantity_by_product[product] += quantity

    # Find best-selling product
    best_seller = max(quantity_by_product.items(), key=lambda x: x[1])

    # Generate report
    with open(output_path, 'w') as f:
        f.write("Sales Summary Report\n")
        f.write("=" * 50 + "\n\n")

        f.write("Revenue by Product:\n")
        f.write("-" * 50 + "\n")
        for product, revenue in sorted(revenue_by_product.items(),
                                      key=lambda x: x[1],
                                      reverse=True):
            f.write(f"{product}: ${revenue:,.2f}\n")

        f.write("\n")
        f.write("Quantity Sold by Product:\n")
        f.write("-" * 50 + "\n")
        for product, quantity in sorted(quantity_by_product.items(),
                                       key=lambda x: x[1],
                                       reverse=True):
            f.write(f"{product}: {quantity:,} units\n")

        f.write("\n")
        f.write("Best-Selling Product:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{best_seller[0]}: {best_seller[1]:,} units\n")

        # Calculate totals
        total_revenue = sum(revenue_by_product.values())
        total_quantity = sum(quantity_by_product.values())

        f.write("\n")
        f.write("Totals:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue: ${total_revenue:,.2f}\n")
        f.write(f"Total Units Sold: {total_quantity:,}\n")


if __name__ == "__main__":
    csv_path = "data/sales.csv"
    output_path = "summary.txt"

    process_sales_data(csv_path, output_path)
    print(f"✅ Summary report generated: {output_path}")
