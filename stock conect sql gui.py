import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ------------------- MySQL Connection -------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="inventory_db"
)
cursor = conn.cursor()

# ------------------- Load Data from SQL -------------------
def load_data():
    global products_df, sales_df, suppliers_df, purchases_df

    # Products
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    products_df = pd.DataFrame(products, columns=["ID","Name","Category","Cost","Price","Stock"])

    # Sales
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    sales_df = pd.DataFrame(sales, columns=["ID","Product","Quantity","Price","Date"])

    # Suppliers
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    suppliers_df = pd.DataFrame(suppliers, columns=["ID","Name","Contact","Email"])

    # Purchases
    cursor.execute("SELECT * FROM purchases")
    purchases = cursor.fetchall()
    purchases_df = pd.DataFrame(purchases, columns=["ID","Product","Supplier","Quantity","Price","Date"])

load_data()

# ------------------- Tkinter App -------------------
class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Inventory & Sales System")
        self.geometry("1300x800")
        self.configure(bg="#f0f0f0")

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Build all tabs
        self._build_products_tab()
        self._build_sales_tab()
        self._build_suppliers_tab()
        self._build_purchases_tab()
        self._build_reports_tab()

    # ------------------- Products Tab -------------------
    def _build_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Products")

        frm = ttk.Frame(tab)
        frm.pack(pady=10)
        ttk.Label(frm, text="Name:").grid(row=0, column=0)
        self.prod_name = ttk.Entry(frm)
        self.prod_name.grid(row=0, column=1)
        ttk.Label(frm, text="Category:").grid(row=0, column=2)
        self.prod_cat = ttk.Entry(frm)
        self.prod_cat.grid(row=0, column=3)
        ttk.Label(frm, text="Cost:").grid(row=1, column=0)
        self.prod_cost = ttk.Entry(frm)
        self.prod_cost.grid(row=1, column=1)
        ttk.Label(frm, text="Price:").grid(row=1, column=2)
        self.prod_price = ttk.Entry(frm)
        self.prod_price.grid(row=1, column=3)
        ttk.Label(frm, text="Stock:").grid(row=2, column=0)
        self.prod_stock = ttk.Entry(frm)
        self.prod_stock.grid(row=2, column=1)
        ttk.Button(frm, text="Add Product", command=self.add_product).grid(row=2, column=3, pady=10)

        # Table
        cols = ["ID","Name","Category","Cost","Price","Stock"]
        self.tree_products = ttk.Treeview(tab, columns=cols, show="headings")
        for c in cols:
            self.tree_products.heading(c, text=c)
            self.tree_products.column(c, width=120)
        self.tree_products.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_products_table()

    def _refresh_products_table(self):
        self.tree_products.delete(*self.tree_products.get_children())
        for _, row in products_df.iterrows():
            self.tree_products.insert("", tk.END, values=list(row))

    def add_product(self):
        try:
            sql = "INSERT INTO products (name, category, cost, price, stock) VALUES (%s,%s,%s,%s,%s)"
            val = (self.prod_name.get(), self.prod_cat.get(),
                   float(self.prod_cost.get()), float(self.prod_price.get()), int(self.prod_stock.get()))
            cursor.execute(sql, val)
            conn.commit()
            load_data()
            self._refresh_products_table()
            messagebox.showinfo("Success", "Product Added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------- Sales Tab -------------------
    def _build_sales_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sales")

        frm = ttk.Frame(tab)
        frm.pack(pady=10)
        ttk.Label(frm, text="Product:").grid(row=0, column=0)
        self.sale_prod = ttk.Entry(frm)
        self.sale_prod.grid(row=0, column=1)
        ttk.Label(frm, text="Quantity:").grid(row=1, column=0)
        self.sale_qty = ttk.Entry(frm)
        self.sale_qty.grid(row=1, column=1)
        ttk.Label(frm, text="Price:").grid(row=2, column=0)
        self.sale_price = ttk.Entry(frm)
        self.sale_price.grid(row=2, column=1)
        ttk.Label(frm, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
        self.sale_date = ttk.Entry(frm)
        self.sale_date.grid(row=3, column=1)
        ttk.Button(frm, text="Add Sale", command=self.add_sale).grid(row=4, column=0, columnspan=2, pady=10)

        # Table
        cols = ["ID","Product","Quantity","Price","Date"]
        self.tree_sales = ttk.Treeview(tab, columns=cols, show="headings")
        for c in cols:
            self.tree_sales.heading(c, text=c)
            self.tree_sales.column(c, width=120)
        self.tree_sales.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_sales_table()

    def _refresh_sales_table(self):
        self.tree_sales.delete(*self.tree_sales.get_children())
        for _, row in sales_df.iterrows():
            self.tree_sales.insert("", tk.END, values=list(row))

    def add_sale(self):
        try:
            sql = "INSERT INTO sales (product, quantity, price, date) VALUES (%s,%s,%s,%s)"
            val = (self.sale_prod.get(), int(self.sale_qty.get()), float(self.sale_price.get()), self.sale_date.get())
            cursor.execute(sql, val)
            conn.commit()
            load_data()
            self._refresh_sales_table()
            messagebox.showinfo("Success", "Sale Added")
            self.update_reports()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------- Suppliers Tab -------------------
    def _build_suppliers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Suppliers")

        frm = ttk.Frame(tab)
        frm.pack(pady=10)
        ttk.Label(frm, text="Name:").grid(row=0, column=0)
        self.sup_name = ttk.Entry(frm)
        self.sup_name.grid(row=0, column=1)
        ttk.Label(frm, text="Contact:").grid(row=0, column=2)
        self.sup_contact = ttk.Entry(frm)
        self.sup_contact.grid(row=0, column=3)
        ttk.Label(frm, text="Email:").grid(row=1, column=0)
        self.sup_email = ttk.Entry(frm)
        self.sup_email.grid(row=1, column=1)
        ttk.Button(frm, text="Add Supplier", command=self.add_supplier).grid(row=1, column=3, pady=10)

        cols = ["ID","Name","Contact","Email"]
        self.tree_suppliers = ttk.Treeview(tab, columns=cols, show="headings")
        for c in cols:
            self.tree_suppliers.heading(c, text=c)
            self.tree_suppliers.column(c, width=150)
        self.tree_suppliers.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_suppliers_table()

    def _refresh_suppliers_table(self):
        self.tree_suppliers.delete(*self.tree_suppliers.get_children())
        for _, row in suppliers_df.iterrows():
            self.tree_suppliers.insert("", tk.END, values=list(row))

    def add_supplier(self):
        try:
            sql = "INSERT INTO suppliers (name, contact, email) VALUES (%s,%s,%s)"
            val = (self.sup_name.get(), self.sup_contact.get(), self.sup_email.get())
            cursor.execute(sql, val)
            conn.commit()
            load_data()
            self._refresh_suppliers_table()
            messagebox.showinfo("Success", "Supplier Added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------- Purchases Tab -------------------
    def _build_purchases_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Purchases")

        frm = ttk.Frame(tab)
        frm.pack(pady=10)
        ttk.Label(frm, text="Product:").grid(row=0, column=0)
        self.pur_prod = ttk.Entry(frm)
        self.pur_prod.grid(row=0, column=1)
        ttk.Label(frm, text="Supplier:").grid(row=0, column=2)
        self.pur_supplier = ttk.Entry(frm)
        self.pur_supplier.grid(row=0, column=3)
        ttk.Label(frm, text="Quantity:").grid(row=1, column=0)
        self.pur_qty = ttk.Entry(frm)
        self.pur_qty.grid(row=1, column=1)
        ttk.Label(frm, text="Price:").grid(row=1, column=2)
        self.pur_price = ttk.Entry(frm)
        self.pur_price.grid(row=1, column=3)
        ttk.Label(frm, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.pur_date = ttk.Entry(frm)
        self.pur_date.grid(row=2, column=1)
        ttk.Button(frm, text="Add Purchase", command=self.add_purchase).grid(row=2, column=3, pady=10)

        cols = ["ID","Product","Supplier","Quantity","Price","Date"]
        self.tree_purchases = ttk.Treeview(tab, columns=cols, show="headings")
        for c in cols:
            self.tree_purchases.heading(c, text=c)
            self.tree_purchases.column(c, width=120)
        self.tree_purchases.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_purchases_table()

    def _refresh_purchases_table(self):
        self.tree_purchases.delete(*self.tree_purchases.get_children())
        for _, row in purchases_df.iterrows():
            self.tree_purchases.insert("", tk.END, values=list(row))

    def add_purchase(self):
        try:
            sql = "INSERT INTO purchases (product, supplier, quantity, price, date) VALUES (%s,%s,%s,%s,%s)"
            val = (self.pur_prod.get(), self.pur_supplier.get(), int(self.pur_qty.get()),
                   float(self.pur_price.get()), self.pur_date.get())
            cursor.execute(sql, val)
            conn.commit()
            load_data()
            self._refresh_purchases_table()
            messagebox.showinfo("Success", "Purchase Added")
            self.update_reports()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------- Reports Tab -------------------
    def _build_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")

        self.fig, self.axs = plt.subplots(2,2, figsize=(12,9))
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        def on_tab_changed(event):
            selected = event.widget.tab('current')['text']
            if selected == "Reports":
                self.update_reports()
        self.notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    def update_reports(self):
        for ax_row in self.axs:
            for ax in ax_row:
                ax.clear()

        if not sales_df.empty:
            sales_df["Date"] = pd.to_datetime(sales_df["Date"])
            purchases_df["Date"] = pd.to_datetime(purchases_df["Date"])

            # Monthly Revenue
            revenue = sales_df.groupby(sales_df["Date"].dt.to_period("M"))["Price"].sum()
            self.axs[0][0].plot(revenue.index.astype(str), revenue.values, marker='o', color='green')
            self.axs[0][0].set_title("Monthly Revenue")

            # Monthly Purchase Cost
            purchase_cost = purchases_df.groupby(purchases_df["Date"].dt.to_period("M"))["Price"].sum()
            self.axs[0][1].plot(purchase_cost.index.astype(str), purchase_cost.values, marker='o', color='red')
            self.axs[0][1].set_title("Monthly Purchase Cost")

            # Monthly Profit
            all_months = revenue.index.union(purchase_cost.index)
            profit = revenue.reindex(all_months, fill_value=0) - purchase_cost.reindex(all_months, fill_value=0)
            self.axs[1][0].bar(profit.index.astype(str), profit.values, color='blue')
            self.axs[1][0].set_title("Monthly Profit")

            # Top Selling Products
            top_products = sales_df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5)
            self.axs[1][1].bar(top_products.index, top_products.values, color='orange')
            self.axs[1][1].set_title("Top Selling Products")
        else:
            for ax_row in self.axs:
                for ax in ax_row:
                    ax.text(0.5,0.5,"No Data", ha="center")

        self.fig.tight_layout()
        self.canvas.draw()


# ------------------- Run App -------------------
if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
    conn.close()
