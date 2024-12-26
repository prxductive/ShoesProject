import tkinter as tk
from tkinter import ttk
from db import DBManager
from tkinter import messagebox

class AppGUI:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.root.title("Управление продажей обуви")
        self.root.state('zoomed')
        self.root.title_label = tk.Label(self.root, text="Управление продажей обуви", font=("Arial", 16))
        self.root.title_label.pack(pady=10)
        self.root.title_label.place(relx=0.5, rely=0, anchor="n")

        self._create_main_frame()
        self.report_window = None
        self.add_stock_window = None
        self.add_order_window = None
        self.add_sale_window = None

    def _create_main_frame(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=50)

        self._create_stock_tab()
        self._create_orders_tab()
        self._create_sales_tab()

        report_button = tk.Button(self.root, text="Отчетность", command=self._open_reports_window)
        report_button.pack(padx=10, pady=10, anchor="ne")
        report_button.place(relx=0.99, rely=0, anchor="ne")


    def _create_stock_tab(self):
        stock_tab = ttk.Frame(self.notebook)
        self.notebook.add(stock_tab, text='Склад')

        columns = ("Код продукта", "Название продукта", "Материал", "Вид обуви", "Цвет", "Количество", "Стоимость")
        self.stock_tree = ttk.Treeview(stock_tab, columns=columns, show='headings')

        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=120)

        self.stock_tree.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Button(stock_tab, text="Новая запись", command=self._open_add_stock_window).pack(pady=10, anchor="se", padx=20, side="right")

        self.stock_tree.bind("<Delete>", lambda event: self._delete_record(event, self.stock_tree, "products", "product_id"))
        self._update_stock_table()


    def _create_orders_tab(self):
        orders_tab = ttk.Frame(self.notebook)
        self.notebook.add(orders_tab, text='Заказы')

        columns = ("Код заказа", "Покупатель", "Название продукта", "Количество", "Статус")
        self.orders_tree = ttk.Treeview(orders_tab, columns=columns, show='headings')

        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=120)

        self.orders_tree.pack(expand=True, fill='both', padx=20, pady=20)
        tk.Button(orders_tab, text="Новая запись", command=self._open_add_order_window).pack(pady=10, anchor="se", padx=20, side="right")
        self.orders_tree.bind("<Delete>", lambda event: self._delete_record(event, self.orders_tree, "orders", "order_id"))
        self._update_orders_table()


    def _create_sales_tab(self):
        sales_tab = ttk.Frame(self.notebook)
        self.notebook.add(sales_tab, text='Продажа')

        columns = ("Код операции", "Код заказа", "Название продукта", "Количество", "Сумма")
        self.sales_tree = ttk.Treeview(sales_tab, columns=columns, show='headings')

        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=120)

        self.sales_tree.pack(expand=True, fill='both', padx=20, pady=20)
        tk.Button(sales_tab, text="Новая запись", command=self._open_add_sale_window).pack(pady=10, anchor="se", padx=20, side="right")
        self.sales_tree.bind("<Delete>", lambda event: self._delete_record(event, self.sales_tree, "sales", "sale_id"))
        self._update_sales_table()

    def _open_reports_window(self):
        if self.report_window is None or not tk.Toplevel.winfo_exists(self.report_window):
            self.report_window = tk.Toplevel(self.root)
            self.report_window.title("Отчетность")
            self.report_window.state('zoomed')
            tk.Label(self.report_window, text="Здесь будет отчет", font=("Arial", 12)).pack(padx=10, pady=10)

    def _open_add_stock_window(self):
        if self.add_stock_window is None or not tk.Toplevel.winfo_exists(self.add_stock_window):
            self.add_stock_window = tk.Toplevel(self.root)
            add_stock_window = self.add_stock_window
            add_stock_window.title("Новая запись в склад")

            # Центрируем окно
            add_stock_window.update_idletasks()
            width = add_stock_window.winfo_width()
            height = add_stock_window.winfo_height()
            screen_width = add_stock_window.winfo_screenwidth()
            screen_height = add_stock_window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            add_stock_window.wm_geometry(f'+{int(x)}+{int(y)}')

            tk.Label(add_stock_window, text="Название продукта", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
            product_name_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            product_name_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_stock_window, text="Материал", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
            material_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            material_entry.grid(row=2, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_stock_window, text="Вид обуви", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
            shoe_type_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            shoe_type_entry.grid(row=3, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_stock_window, text="Цвет", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
            color_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            color_entry.grid(row=4, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_stock_window, text="Количество", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
            quantity_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            quantity_entry.grid(row=5, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_stock_window, text="Стоимость", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
            price_entry = tk.Entry(add_stock_window, font=("Arial", 12))
            price_entry.grid(row=6, column=1, sticky="e", padx=10, pady=5)
            error_label = tk.Label(add_stock_window, text="", font=("Arial", 12), fg="red")
            error_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

            tk.Button(add_stock_window, text="Записать и закрыть", command= lambda: self._add_stock(
                product_name_entry.get(),
                material_entry.get(),
                shoe_type_entry.get(),
                color_entry.get(),
                quantity_entry.get(),
                price_entry.get(),
                add_stock_window,
                error_label), font=("Arial", 12)).grid(row=7, column=0, columnspan=2, pady=10, sticky="ew", padx=10)
            add_stock_window.focus()
    def _open_add_order_window(self):
          if self.add_order_window is None or not tk.Toplevel.winfo_exists(self.add_order_window):
            self.add_order_window = tk.Toplevel(self.root)
            add_order_window = self.add_order_window
            add_order_window.title("Новая запись в заказы")

             # Центрируем окно
            add_order_window.update_idletasks()
            width = add_order_window.winfo_width()
            height = add_order_window.winfo_height()
            screen_width = add_order_window.winfo_screenwidth()
            screen_height = add_order_window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            add_order_window.wm_geometry(f'+{int(x)}+{int(y)}')

            tk.Label(add_order_window, text="Покупатель", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
            customer_name_entry = tk.Entry(add_order_window, font=("Arial", 12))
            customer_name_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_order_window, text="Название продукта", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
            product_name_entry = ttk.Combobox(add_order_window, font=("Arial", 12), values=self._get_products_from_stock())
            product_name_entry.grid(row=2, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_order_window, text="Количество", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
            quantity_entry = tk.Entry(add_order_window, font=("Arial", 12))
            quantity_entry.grid(row=3, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_order_window, text="Статус", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
            status_combobox = ttk.Combobox(add_order_window, values=("Выполнен", "Не выполнен"), font=("Arial", 12))
            status_combobox.grid(row=4, column=1, sticky="e", padx=10, pady=5)
            error_label = tk.Label(add_order_window, text="", font=("Arial", 12), fg="red")
            error_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

            tk.Button(add_order_window, text="Записать и закрыть", command= lambda: self._add_order(
                customer_name_entry.get(),
                product_name_entry.get().lower(),
                quantity_entry.get(),
                status_combobox.get(),
                add_order_window,
                error_label), font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", padx=10)
            add_order_window.focus()
    def _open_add_sale_window(self):
        if self.add_sale_window is None or not tk.Toplevel.winfo_exists(self.add_sale_window):
            self.add_sale_window = tk.Toplevel(self.root)
            add_sale_window = self.add_sale_window
            add_sale_window.title("Новая запись в продажи")
            # Центрируем окно
            add_sale_window.update_idletasks()
            width = add_sale_window.winfo_width()
            height = add_sale_window.winfo_height()
            screen_width = add_sale_window.winfo_screenwidth()
            screen_height = add_sale_window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            add_sale_window.wm_geometry(f'+{int(x)}+{int(y)}')

            tk.Label(add_sale_window, text="Код заказа", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
            order_id_entry = tk.Entry(add_sale_window, font=("Arial", 12))
            order_id_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_sale_window, text="Название продукта", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
            product_name_entry = ttk.Combobox(add_sale_window, font=("Arial", 12), values=self._get_products_from_stock())
            product_name_entry.grid(row=2, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_sale_window, text="Количество", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
            quantity_entry = tk.Entry(add_sale_window, font=("Arial", 12))
            quantity_entry.grid(row=3, column=1, sticky="e", padx=10, pady=5)
            tk.Label(add_sale_window, text="Сумма", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
            total_amount_entry = tk.Entry(add_sale_window, font=("Arial", 12))
            total_amount_entry.grid(row=4, column=1, sticky="e", padx=10, pady=5)
            error_label = tk.Label(add_sale_window, text="", font=("Arial", 12), fg="red")
            error_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

            tk.Button(add_sale_window, text="Записать и закрыть", command= lambda: self._add_sale(
                order_id_entry.get(),
                product_name_entry.get().lower(),
                quantity_entry.get(),
                total_amount_entry.get(),
                add_sale_window,
                error_label), font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", padx=10)
            add_sale_window.focus()
    def _add_stock(self, product_name, material, shoe_type, color, quantity, price, window, error_label):
        query = "INSERT INTO products ( product_name, material, shoe_type, color, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (product_name, material, shoe_type, color, quantity, price)
        if self.db_manager.execute_query(query, params):
          window.destroy()
          self._update_stock_table()
        else:
            error_label.config(text="Ошибка при добавлении записи")
    def _add_order(self, customer_name, product_name, quantity, status, window, error_label):
        if product_name.lower() not in [row.lower() for row in self._get_products_from_stock()]:
             error_label.config(text="Такого продукта нет на складе!", wraplength=400)
             return
        query = "INSERT INTO orders (customer_name, product_name, quantity, order_status) VALUES (%s, %s, %s, %s)"
        params = (customer_name, product_name, quantity, status)
        if self.db_manager.execute_query(query, params):
            window.destroy()
            self._update_orders_table()
        else:
            error_label.config(text="Ошибка при добавлении записи")
    def _add_sale(self, order_id, product_name, quantity, total_amount, window, error_label):
        if product_name.lower() not in [row.lower() for row in self._get_products_from_stock()]:
              error_label.config(text="Такого продукта нет на складе!", wraplength=400)
              return
        query = "INSERT INTO sales (order_id, product_name, quantity, total_amount) VALUES (%s, %s, %s, %s)"
        params = (order_id, product_name, quantity, total_amount)
        if self.db_manager.execute_query(query, params):
             window.destroy()
             self._update_sales_table()
        else:
             error_label.config(text="Ошибка при добавлении записи")
    def _delete_record(self, event, tree, table, id_col):
        selected_item = tree.selection()
        if selected_item:
            record_id = tree.item(selected_item, 'values')[0]
            try:
                 if table == "products":
                    if self._is_product_used_in_orders(record_id) or self._is_product_used_in_sales(record_id):
                        tk.messagebox.showerror("Ошибка", "Невозможно удалить продукт, так как он используется в заказах или продажах")
                        return
                 elif table == "orders":
                     if self._is_order_used_in_sales(record_id):
                         tk.messagebox.showerror("Ошибка", "Невозможно удалить заказ, так как он используется в продажах")
                         return
                 query = f"DELETE FROM {table} WHERE {id_col} = %s"
                 if not self.db_manager.execute_query(query, (record_id,)):
                    tk.messagebox.showerror("Ошибка", f"Не удалось удалить запись c ID {record_id}")
                 else:
                     tree.delete(selected_item)
            except Exception as e:
              tk.messagebox.showerror("Ошибка", f"Невозможно удалить запись, так как она связана с другими таблицами")
    def _is_product_used_in_orders(self, product_id):
        query = "SELECT COUNT(*) FROM orders WHERE product_name = (SELECT product_name FROM products WHERE product_id = %s)"
        params = (product_id,)
        result = self.db_manager.fetch_all(query,params)
        return result and result[0][0] > 0
    def _is_product_used_in_sales(self, product_id):
        query = "SELECT COUNT(*) FROM sales WHERE product_name = (SELECT product_name FROM products WHERE product_id = %s)"
        params = (product_id,)
        result = self.db_manager.fetch_all(query, params)
        return result and result[0][0] > 0
    def _is_order_used_in_sales(self, order_id):
        query = "SELECT COUNT(*) FROM sales WHERE order_id = %s"
        params = (order_id,)
        result = self.db_manager.fetch_all(query, params)
        return result and result[0][0] > 0
    def _get_products_from_stock(self):
        query = "SELECT product_name FROM products"
        rows = self.db_manager.fetch_all(query)
        if rows:
          return [row[0] for row in rows]
        return []

    def _update_stock_table(self):
        for row in self.stock_tree.get_children():
            self.stock_tree.delete(row)
        query = "SELECT * FROM products"
        rows = self.db_manager.fetch_all(query)
        for row in rows:
             self.stock_tree.insert('', 'end', values=row)
    def _update_orders_table(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        query = "SELECT * FROM orders"
        rows = self.db_manager.fetch_all(query)
        for row in rows:
             self.orders_tree.insert('', 'end', values=row)
    def _update_sales_table(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)
        query = "SELECT * FROM sales"
        rows = self.db_manager.fetch_all(query)
        for row in rows:
            self.sales_tree.insert('', 'end', values=row)