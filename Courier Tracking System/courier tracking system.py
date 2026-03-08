# courier_tracking.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
import csv

# ======== CONFIGURE DB CONNECTION HERE ========
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'RAHUL123',  # <-- set your MySQL root/password
    'database': 'courier_db'
}
# ==============================================

STATUS_OPTIONS = ['Pending','Packaging','Shipped','In Transit','Out for Delivery','Delivered','Returned']

class CourierDB:
    def __init__(self, cfg):
        self.cfg = cfg
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.cfg)
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", f"Could not connect to database:\n{e}")
            raise

    def fetchall(self, query, params=None):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows

    def execute(self, query, params=None):
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        self.conn.commit()
        last = cur.lastrowid
        cur.close()
        return last

    def close(self):
        if self.conn:
            self.conn.close()

class CourierApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Courier Tracking System")
        self.geometry("1100x650")
        self.minsize(1000, 600)
        self.create_widgets()
        self.load_shipments()

    def create_widgets(self):
        # --- top frame : form ---
        frm_top = ttk.Frame(self, padding=10)
        frm_top.pack(fill='x')

        # form fields
        labels = ['Tracking No', 'Sender', 'Receiver', 'Origin', 'Destination', 'Package Date (YYYY-MM-DD)', 'Expected Delivery (YYYY-MM-DD)', 'Status', 'Current Location']
        self.entries = {}
        for i, lab in enumerate(labels):
            row = i // 3
            col = (i % 3) * 2
            ttk.Label(frm_top, text=lab).grid(row=row, column=col, sticky='w', padx=4, pady=4)
            if lab == 'Status':
                ent = ttk.Combobox(frm_top, values=STATUS_OPTIONS, state='readonly')
                ent.set(STATUS_OPTIONS[0])
            else:
                ent = ttk.Entry(frm_top)
            ent.grid(row=row, column=col+1, sticky='we', padx=4, pady=4)
            self.entries[lab] = ent
        # manager notes area
        ttk.Label(frm_top, text="Manager Notes").grid(row=3, column=6, sticky='nw', padx=6)
        self.txt_notes = tk.Text(frm_top, height=5, width=40)
        self.txt_notes.grid(row=3, column=7, rowspan=2, sticky='we', padx=6, pady=4)

        # action buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=10)
        ttk.Button(btn_frame, text="Add Shipment", command=self.add_shipment).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_shipment).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_shipment).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Set Status -> Packaging", command=lambda: self.set_status_bulk('Packaging')).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Set Status -> Shipped", command=lambda: self.set_status_bulk('Shipped')).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Set Status -> In Transit", command=lambda: self.set_status_bulk('In Transit')).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Set Status -> Out for Delivery", command=lambda: self.set_status_bulk('Out for Delivery')).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Set Status -> Delivered", command=lambda: self.set_status_bulk('Delivered')).pack(side='left', padx=6)

        # search/filter
        search_frame = ttk.Frame(self)
        search_frame.pack(fill='x', padx=10, pady=8)
        ttk.Label(search_frame, text="Search Tracking No:").pack(side='left', padx=4)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side='left', padx=4)
        ttk.Button(search_frame, text="Search", command=self.search_tracking).pack(side='left', padx=4)
        ttk.Button(search_frame, text="Show All", command=self.load_shipments).pack(side='left', padx=4)
        ttk.Label(search_frame, text="Filter by Status:").pack(side='left', padx=10)
        self.filter_status = ttk.Combobox(search_frame, values=['All']+STATUS_OPTIONS, state='readonly')
        self.filter_status.set('All')
        self.filter_status.pack(side='left', padx=4)
        ttk.Button(search_frame, text="Apply", command=self.filter_by_status).pack(side='left', padx=4)
        ttk.Button(search_frame, text="Export CSV", command=self.export_csv).pack(side='right', padx=4)

        # Treeview list
        cols = ('id','tracking_no','sender_name','receiver_name','origin','destination','package_date','expected_delivery','status','current_location','manager_notes')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', selectmode='extended')
        headings = {
            'id':'ID','tracking_no':'Tracking No','sender_name':'Sender','receiver_name':'Receiver',
            'origin':'Origin','destination':'Destination','package_date':'Pack Date',
            'expected_delivery':'Expected Delivery','status':'Status','current_location':'Current Location','manager_notes':'Manager Notes'
        }
        for c in cols:
            self.tree.heading(c, text=headings[c])
            if c in ('manager_notes','current_location'):
                self.tree.column(c, width=200, anchor='w')
            elif c in ('sender_name','receiver_name','origin','destination'):
                self.tree.column(c, width=120, anchor='w')
            elif c in ('tracking_no',):
                self.tree.column(c, width=110, anchor='center')
            else:
                self.tree.column(c, width=90, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=6)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # status bar
        self.status_bar = ttk.Label(self, text="Ready", anchor='w')
        self.status_bar.pack(fill='x', side='bottom')

    # ---- DB actions ----
    def add_shipment(self):
        data = self._gather_form()
        if not data: return
        try:
            q = """INSERT INTO shipments (tracking_no, sender_name, receiver_name, origin, destination, package_date, expected_delivery, status, current_location, manager_notes)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            params = (data['tracking_no'], data['sender_name'], data['receiver_name'], data['origin'], data['destination'],
                      data['package_date'], data['expected_delivery'], data['status'], data['current_location'], data['manager_notes'])
            self.db.execute(q, params)
            messagebox.showinfo("Success", "Shipment added.")
            self.load_shipments()
            self._clear_form()
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Could not add shipment: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_shipment(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a row to update.")
            return
        row_id = self.tree.item(sel[0])['values'][0]
        data = self._gather_form()
        if not data: return
        q = """UPDATE shipments SET tracking_no=%s, sender_name=%s, receiver_name=%s, origin=%s, destination=%s,
               package_date=%s, expected_delivery=%s, status=%s, current_location=%s, manager_notes=%s WHERE id=%s"""
        params = (data['tracking_no'], data['sender_name'], data['receiver_name'], data['origin'], data['destination'],
                  data['package_date'], data['expected_delivery'], data['status'], data['current_location'], data['manager_notes'], row_id)
        try:
            self.db.execute(q, params)
            messagebox.showinfo("Updated", "Shipment updated.")
            self.load_shipments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_shipment(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select row(s) to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete {len(sel)} selected record(s)?"): return
        try:
            cur = self.db.conn.cursor()
            for item in sel:
                row_id = self.tree.item(item)['values'][0]
                cur.execute("DELETE FROM shipments WHERE id=%s", (row_id,))
            self.db.conn.commit()
            cur.close()
            self.load_shipments()
            messagebox.showinfo("Deleted", "Selected records deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_status_bulk(self, status):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select row(s) to change status.")
            return
        try:
            cur = self.db.conn.cursor()
            for item in sel:
                row_id = self.tree.item(item)['values'][0]
                cur.execute("UPDATE shipments SET status=%s WHERE id=%s", (status, row_id))
            self.db.conn.commit()
            cur.close()
            self.load_shipments()
            self.status_bar.config(text=f"Set {len(sel)} record(s) to '{status}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_tracking(self):
        key = self.search_var.get().strip()
        if not key:
            messagebox.showinfo("Input", "Enter tracking number to search.")
            return
        q = "SELECT * FROM shipments WHERE tracking_no LIKE %s ORDER BY created_at DESC"
        rows = self.db.fetchall(q, (f"%{key}%",))
        self._populate_tree(rows)

    def filter_by_status(self):
        status = self.filter_status.get()
        if status == 'All' or not status:
            self.load_shipments()
            return
        q = "SELECT * FROM shipments WHERE status=%s ORDER BY created_at DESC"
        rows = self.db.fetchall(q, (status,))
        self._populate_tree(rows)

    def load_shipments(self):
        q = "SELECT * FROM shipments ORDER BY created_at DESC"
        rows = self.db.fetchall(q)
        self._populate_tree(rows)

    def export_csv(self):
        rows = []
        for item in self.tree.get_children():
            rows.append(self.tree.item(item)['values'])
        if not rows:
            messagebox.showinfo("No Data", "No rows to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not file:
            return
        headers = ['ID','Tracking No','Sender','Receiver','Origin','Destination','Package Date','Expected Delivery','Status','Current Location','Manager Notes']
        try:
            with open(file, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(headers)
                for r in rows:
                    w.writerow(r)
            messagebox.showinfo("Exported", f"Exported {len(rows)} rows to {file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---- Helpers ----
    def _populate_tree(self, rows):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            vals = (
                r['id'], r['tracking_no'], r['sender_name'] or '', r['receiver_name'] or '',
                r['origin'] or '', r['destination'] or '',
                r['package_date'].isoformat() if r['package_date'] else '',
                r['expected_delivery'].isoformat() if r['expected_delivery'] else '',
                r['status'] or '', r['current_location'] or '', (r['manager_notes'] or '')[:200]
            )
            self.tree.insert('', 'end', values=vals)
        self.status_bar.config(text=f"Loaded {len(rows)} record(s).")

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])['values']
        # map to form
        mapping = {
            'Tracking No': item[1], 'Sender': item[2], 'Receiver': item[3],
            'Origin': item[4], 'Destination': item[5], 'Package Date (YYYY-MM-DD)': item[6],
            'Expected Delivery (YYYY-MM-DD)': item[7], 'Status': item[8], 'Current Location': item[9]
        }
        for k, v in mapping.items():
            ent = self.entries[k]
            ent.delete(0, tk.END)
            ent.insert(0, v)
        # notes
        self.txt_notes.delete('1.0', tk.END)
        self.txt_notes.insert('1.0', item[10] or '')

    def _gather_form(self):
        t = self.entries['Tracking No'].get().strip()
        if not t:
            messagebox.showwarning("Input", "Tracking No is required.")
            return None
        def get(k): return self.entries[k].get().strip()
        data = {
            'tracking_no': t,
            'sender_name': get('Sender'),
            'receiver_name': get('Receiver'),
            'origin': get('Origin'),
            'destination': get('Destination'),
            'package_date': get('Package Date (YYYY-MM-DD)'),
            'expected_delivery': get('Expected Delivery (YYYY-MM-DD)'),
            'status': get('Status') or 'Pending',
            'current_location': get('Current Location'),
            'manager_notes': self.txt_notes.get('1.0', tk.END).strip()
        }
        # validate dates (basic)
        for date_field in ('package_date','expected_delivery'):
            if data[date_field]:
                try:
                    datetime.strptime(data[date_field], "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Date format", f"{date_field.replace('_',' ').title()} must be YYYY-MM-DD")
                    return None
        return data

    def _clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)
        self.entries['Status'].set(STATUS_OPTIONS[0])
        self.txt_notes.delete('1.0', tk.END)

if __name__ == '__main__':
    # attempt to connect and run
    try:
        db = CourierDB(DB_CONFIG)
    except Exception:
        print("Could not connect to DB. Check credentials and that 'courier_db' exists.")
        raise
    app = CourierApp(db)
    app.mainloop()
    db.close()
