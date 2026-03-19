import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ipaddress
import math
import pandas as pd
from fpdf import FPDF
import sys
import os
import ctypes
from datetime import datetime
from PIL import Image, ImageTk 

try:
    myappid = 'wilson.vlsm.calculator.dualstack.v5' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VLSMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VLSMS Dual-Stack Calculator (IPv4/IPv6) - Wpinzon-ASIR")
        self.root.geometry("870x600")
        self.root.resizable(True, True) 
        self.root.minsize(850, 580)

        # --- SISTEMA DE SCROLL GENERAL PARA LA VENTANA ---
        self.main_canvas = tk.Canvas(root, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def _on_canvas_configure(e):
            self.main_canvas.itemconfig(self.canvas_window, width=e.width)

        self.main_canvas.bind("<Configure>", _on_canvas_configure)
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Carga de Icono
        self.app_icon_photo = None 
        try:
            icon_p = resource_path("wil.ico")
            if os.path.exists(icon_p):
                self.root.iconbitmap(icon_p)
                img_pil = Image.open(icon_p).resize((32, 32), Image.Resampling.LANCZOS)
                self.app_icon_photo = ImageTk.PhotoImage(img_pil)
                self.root.iconphoto(True, self.app_icon_photo)
        except:
            pass
            
        self.vlans_list = []
        self.calculos_realizados = []
        self.historial_data = []
        self.edit_index = None

        # --- CONTENIDO DENTRO DEL FRAME DESPLAZABLE ---
        
        # 1. Red Base
        top = ttk.LabelFrame(self.scrollable_frame, text=" 1. Red Base (IPv4/IPv6) ")
        top.pack(side="top", fill="x", padx=10, pady=5)
        self.ent_red_base = ttk.Entry(top, width=35)
        self.ent_red_base.pack(side="left", padx=5, pady=5)
        self.ent_red_base.insert(0, "10.0.0.0/8")
        ttk.Label(top, text="Formato: 192.168.1.0/24 o 2001:db8::/32", font=("Arial", 8, "italic")).pack(side="left", padx=5)

        # 2. Gestión VLANs
        form = ttk.LabelFrame(self.scrollable_frame, text=" 2. Gestión VLANs ")
        form.pack(side="top", fill="x", padx=10, pady=5)
        
        # Aclaración para el usuario
        ttk.Label(form, text="* PASO 1: Guardar todas las VLANs. PASO 2: Presionar CALCULAR.", 
                  foreground="red", font=("Arial", 8, "bold")).grid(row=0, column=0, columnspan=7, sticky="w", padx=5)

        ttk.Label(form, text="VLAN:").grid(row=1, column=0, padx=2, pady=5)
        self.ent_vlan_name = ttk.Entry(form, width=15)
        self.ent_vlan_name.grid(row=1, column=1, padx=2, pady=5)
        ttk.Label(form, text="Hosts:").grid(row=1, column=2, padx=2, pady=5)
        self.ent_hosts = ttk.Entry(form, width=10)
        self.ent_hosts.grid(row=1, column=3, padx=2, pady=5)
        
        self.btn_save = ttk.Button(form, text="Guardar", command=self.save_vlan)
        self.btn_save.grid(row=1, column=4, padx=5)
        ttk.Button(form, text="Borrar", command=self.delete_vlan).grid(row=1, column=5, padx=5)
        ttk.Button(form, text="CALCULAR", command=self.calculate).grid(row=1, column=6, padx=10)

        # 3. Lista VLANs Agregadas
        list_f = ttk.LabelFrame(self.scrollable_frame, text=" VLANs Agregadas ")
        list_f.pack(side="top", fill="x", padx=10, pady=5)
        
        tree_p_container = ttk.Frame(list_f)
        tree_p_container.pack(fill="x", padx=5, pady=5)
        self.tree_p = ttk.Treeview(tree_p_container, columns=("n", "h"), show="headings", height=4)
        self.tree_p.heading("n", text="VLAN"); self.tree_p.heading("h", text="Hosts")
        self.tree_p.column("n", width=200); self.tree_p.column("h", width=100)
        sc_p = ttk.Scrollbar(tree_p_container, orient="vertical", command=self.tree_p.yview)
        self.tree_p.configure(yscrollcommand=sc_p.set)
        self.tree_p.pack(side="left", fill="x", expand=True)
        sc_p.pack(side="right", fill="y")
        self.tree_p.bind("<Double-1>", self.prepare_edit)

        # 4. Notebook (Pestañas)
        self.nb = ttk.Notebook(self.scrollable_frame)
        self.nb.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        
        # Pestaña Tabla
        self.res_f = ttk.Frame(self.nb); self.nb.add(self.res_f, text=" Tabla ")
        tree_res_container = ttk.Frame(self.res_f)
        tree_res_container.pack(fill="both", expand=True)
        cols = ("v", "req", "net", "mask", "gw", "broadcast", "range")
        self.tree_res = ttk.Treeview(tree_res_container, columns=cols, show="headings", height=8)
        h = ["VLAN", "Req.", "Red", "Máscara", "Gateway", "Broadcast", "Rango"]
        for c, t in zip(cols, h): 
            self.tree_res.heading(c, text=t)
            self.tree_res.column(c, width=110, anchor="center")
        
        sc_res_y = ttk.Scrollbar(tree_res_container, orient="vertical", command=self.tree_res.yview)
        self.tree_res.configure(yscrollcommand=sc_res_y.set)
        self.tree_res.pack(side="left", fill="both", expand=True)
        sc_res_y.pack(side="right", fill="y")

        # Pestaña Comandos
        self.cmd_f = ttk.Frame(self.nb); self.nb.add(self.cmd_f, text=" Comandos Cisco ")
        self.txt_cmd = tk.Text(self.cmd_f, wrap="none", font=("Courier", 9), height=10)
        sc_cmd_y = ttk.Scrollbar(self.cmd_f, orient="vertical", command=self.txt_cmd.yview)
        self.txt_cmd.configure(yscrollcommand=sc_cmd_y.set)
        sc_cmd_y.pack(side="right", fill="y")
        self.txt_cmd.pack(fill="both", expand=True)

        # Pestaña Historial
        self.hist_f = ttk.Frame(self.nb); self.nb.add(self.hist_f, text=" Historial ")
        tree_hist_container = ttk.Frame(self.hist_f)
        tree_hist_container.pack(side="left", fill="both", expand=True)
        self.tree_hist = ttk.Treeview(tree_hist_container, columns=("t", "r"), show="headings", height=8)
        self.tree_hist.heading("t", text="Fecha/Hora"); self.tree_hist.heading("r", text="Red Base")
        sc_hist = ttk.Scrollbar(tree_hist_container, orient="vertical", command=self.tree_hist.yview)
        self.tree_hist.configure(yscrollcommand=sc_hist.set)
        self.tree_hist.pack(side="left", fill="both", expand=True)
        sc_hist.pack(side="right", fill="y")
        ttk.Button(self.hist_f, text="Copiar Sel.", command=self.copy_history_excel).pack(side="right", padx=5, pady=5)

        # 5. Footer (Botones de Exportación)
        exp_f = ttk.Frame(self.scrollable_frame)
        exp_f.pack(side="top", fill="x", padx=10, pady=15)
        ttk.Button(exp_f, text="Exportar Excel", command=self.export_excel).pack(side="left", padx=2)
        ttk.Button(exp_f, text="Exportar PDF", command=self.export_pdf).pack(side="left", padx=2)
        ttk.Button(exp_f, text="Copiar para Excel", command=self.copy_results).pack(side="left", padx=2)
        ttk.Button(exp_f, text="Borrar Todo", command=self.clear_all).pack(side="right", padx=2)

    # --- LÓGICA DE LA APP ---

    def save_vlan(self):
        n, h = self.ent_vlan_name.get().strip(), self.ent_hosts.get().strip()
        if n and h.isdigit():
            if self.edit_index is not None:
                self.vlans_list[self.edit_index] = {"nombre": n, "hosts": int(h)}
                self.edit_index = None; self.btn_save.config(text="Guardar")
            else:
                self.vlans_list.append({"nombre": n, "hosts": int(h)})
            self.refresh_list(); self.ent_vlan_name.delete(0, tk.END); self.ent_hosts.delete(0, tk.END)

    def prepare_edit(self, e):
        sel = self.tree_p.selection()
        if sel:
            self.edit_index = self.tree_p.index(sel[0])
            v = self.vlans_list[self.edit_index]
            self.ent_vlan_name.delete(0, tk.END); self.ent_vlan_name.insert(0, v['nombre'])
            self.ent_hosts.delete(0, tk.END); self.ent_hosts.insert(0, str(v['hosts']))
            self.btn_save.config(text="Actualizar")

    def delete_vlan(self):
        sel = self.tree_p.selection()
        if sel: del self.vlans_list[self.tree_p.index(sel[0])]; self.refresh_list()

    def refresh_list(self):
        for i in self.tree_p.get_children(): self.tree_p.delete(i)
        for v in self.vlans_list: self.tree_p.insert("", "end", values=(v['nombre'], v['hosts']))

    def clear_all(self):
        self.vlans_list, self.calculos_realizados = [], []
        self.refresh_list(); [self.tree_res.delete(i) for i in self.tree_res.get_children()]
        self.txt_cmd.delete("1.0", tk.END)

    def calculate(self):
        if not self.vlans_list:
            messagebox.showwarning("Atención", "Debe guardar al menos una VLAN antes de calcular.")
            return
        
        red_in = self.ent_red_base.get().strip()
        try:
            net = ipaddress.ip_network(red_in, strict=False)
            [self.tree_res.delete(i) for i in self.tree_res.get_children()]
            self.calculos_realizados = []
            vlans = sorted(self.vlans_list, key=lambda x: x['hosts'], reverse=True)
            curr = net.network_address
            script = "enable\nconf t\n"
            
            for i, v in enumerate(vlans, 10):
                if net.version == 4:
                    p = 32 - math.ceil(math.log2(v['hosts'] + 2))
                    sub = ipaddress.IPv4Network((curr, p))
                    ips = list(sub.hosts())
                    res = {"V": v['nombre'], "H": v['hosts'], "N": str(sub.network_address), "M": f"/{p}", "G": str(ips[0]), "B": str(sub.broadcast_address), "R": f"{ips[1]}-{ips[-1]}"}
                    script += f"vlan {i}\n name {v['nombre']}\nint vlan {i}\n ip address {res['G']} {sub.netmask}\n no shut\nexit\n"
                    curr = sub.broadcast_address + 1
                else:
                    prefix = 64
                    sub = ipaddress.IPv6Network((curr, prefix), strict=False)
                    res = {"V": v['nombre'], "H": v['hosts'], "N": str(sub.network_address), "M": f"/{prefix}", "G": str(sub.network_address + 1), "B": "N/A", "R": f"{sub.network_address + 2}-{sub.broadcast_address}"}
                    script += f"ipv6 unicast-routing\nvlan {i}\n name {v['nombre']}\nint vlan {i}\n ipv6 address {res['G']}/{prefix}\n no shut\nexit\n"
                    curr = sub.network_address + (2**(128-prefix))

                self.calculos_realizados.append(res); self.tree_res.insert("", "end", values=list(res.values()))
            
            self.txt_cmd.delete("1.0", tk.END); self.txt_cmd.insert("1.0", script)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.historial_data.append({"fecha": ts, "red": red_in, "datos": list(self.calculos_realizados)})
            self.tree_hist.insert("", 0, values=(ts, red_in))
        except Exception as e: messagebox.showerror("Error", str(e))

    def _to_clipboard(self, data):
        if not data: return
        h = "VLAN\tHosts\tRed\tMáscara\tGateway\tBroadcast\tRango"
        b = "\n".join(["\t".join(str(v) for v in r.values()) for r in data])
        self.root.clipboard_clear(); self.root.clipboard_append(h + "\n" + b)

    def copy_results(self): 
        self._to_clipboard(self.calculos_realizados); messagebox.showinfo("Copiado", "Copiado para Excel.")

    def copy_history_excel(self):
        sel = self.tree_hist.selection()
        if sel:
            fecha = self.tree_hist.item(sel[0])['values'][0]
            for h in self.historial_data:
                if h['fecha'] == fecha: self._to_clipboard(h['datos']); break

    def export_excel(self):
        if not self.calculos_realizados: return
        p = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if p: pd.DataFrame(self.calculos_realizados).to_excel(p, index=False)

    def export_pdf(self):
        if not self.calculos_realizados: return
        p = filedialog.asksaveasfilename(defaultextension=".pdf")
        if p:
            pdf = FPDF(orientation='L', unit='mm', format='A4'); pdf.add_page(); pdf.set_font("Arial", 'B', 10)
            for r in self.calculos_realizados:
                for v in r.values(): pdf.cell(38, 8, str(v)[:22], 1)
                pdf.ln()
            pdf.output(p)

if __name__ == "__main__":
    root = tk.Tk(); app = VLSMApp(root); root.mainloop()