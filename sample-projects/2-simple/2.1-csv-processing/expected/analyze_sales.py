import csv
from collections import defaultdict

def analyze_sales(csv_path):
    revenue_by_product = defaultdict(float)
    quantity_by_product = defaultdict(int)
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row['product']
            quantity = int(row['quantity'])
            price = float(row['price'])
            
            revenue_by_product[product] += quantity * price
            quantity_by_product[product] += quantity
    
    # Find best seller
    best_seller = max(quantity_by_product.items(), key=lambda x: x[1])
    
    # Write summary
    with open('summary.txt', 'w') as f:
        f.write("Sales Analysis Summary\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Revenue by Product:\n")
        for product, revenue in sorted(revenue_by_product.items(), key=lambda x: -x[1]):
            f.write(f"  {product}: ${revenue:,.2f}\n")
        
        f.write(f"\nBest-Selling Product: {best_seller[0]} ({best_seller[1]} units)\n")

if __name__ == "__main__":
    analyze_sales('data/sales.csv')
    print("Analysis complete. See summary.txt")
