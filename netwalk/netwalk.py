import tkinter as tk
from tkinter import ttk, messagebox
import scapy.all as scapy
from scapy.all import conf
import socket
import json
import threading
import urllib.request
import os
import ctypes
import sys
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Asegúrate de tener 'Pillow' instalado: pip install Pillow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def set_taskbar_icon():
    # Identificador único para que Windows no lo agrupe con Python
    myappid = 'asir.netwalk.scanner.final'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class NetwalkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Netwalk")
        
        # MÉTODO DEFINITIVO PARA EL ICONO
        try:
            icon_path = resource_path("netwalk.ico")
            # 1. Icono de la ventana (título)
            self.root.iconbitmap(icon_path)
            # 2. Icono de la barra de tareas (forzado)
            img = Image.open(icon_path)
            self.icon_img = ImageTk.PhotoImage(img)
            self.root.wm_iconphoto(True, self.icon_img)
        except Exception as e:
            print(f"Error cargando icono: {e}")
        
        self.root.geometry("1100x750")
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="Rango de Red:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.ip_entry = ttk.Entry(header_frame, width=30)
        self.ip_entry.insert(0, "192.168.1.0/24")
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        self.scan_btn = ttk.Button(header_frame, text="🚀 Escanear", command=self.start_scan_thread)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ttk.Button(header_frame, text="💾 Exportar", command=self.export_results, state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        self.graph_btn = ttk.Button(header_frame, text="🌐 Ver Topología", command=self.show_topology, state=tk.DISABLED)
        self.graph_btn.pack(side=tk.LEFT, padx=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Listo")
        self.status_label.pack()

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tree_frame, text="Lista de Dispositivos")
        self.tree = ttk.Treeview(self.tree_frame, columns=("IP", "MAC", "VENDOR", "OS", "PUERTOS"), show='headings')
        for col, text in [("IP", "IP"), ("MAC", "MAC"), ("VENDOR", "Fabricante"), ("OS", "SO"), ("PUERTOS", "Puertos")]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=140)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_device_double_click)
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="Mapa de Red")
        
        self.results = []
        self.gateway_ip = None

    def on_device_double_click(self, event):
        item = self.tree.selection()
        if item:
            ip = self.tree.item(item[0], "values")[0]
            os.system(f'start cmd /k "title Ping {ip} && ping {ip} -t"')

    def scan_network(self, ip_range):
        try:
            self.update_status("Escaneando red...")
            conf.iface = scapy.get_working_if()
            self.gateway_ip = conf.route.route("0.0.0.0")[2]
            arp = scapy.ARP(pdst=ip_range)
            ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            answered = scapy.srp(ether/arp, timeout=2, verbose=False)[0]
            devices = []
            for _, rcv in answered:
                reply = scapy.sr1(scapy.IP(dst=rcv.psrc)/scapy.ICMP(), timeout=0.5, verbose=False)
                ttl = reply.ttl if reply else "???"
                devices.append({"ip": rcv.psrc, "mac": rcv.hwsrc, "ttl": ttl})
            return devices
        except: return []

    def get_vendor(self, mac):
        try:
            url = f"https://api.macvendors.com/{mac}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1) as response:
                return response.read().decode('utf-8')
        except: return "Desconocido"

    def get_os(self, ttl):
        if ttl <= 64: return "Linux/Unix"
        elif ttl <= 128: return "Windows"
        return "Network Dev"

    def scan_ports(self, ip):
        open_p = []
        for port in [22, 80, 443, 3389]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.05)
                if s.connect_ex((ip, port)) == 0: open_p.append(port)
        return open_p

    def start_scan_thread(self):
        self.scan_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        for i in self.tree.get_children(): self.tree.delete(i)
        self.results = []
        threading.Thread(target=self.run_scanner, daemon=True).start()

    def run_scanner(self):
        devices = self.scan_network(self.ip_entry.get())
        total = len(devices)
        for i, d in enumerate(devices):
            self.update_status(f"Analizando {d['ip']}...")
            d['vendor'] = self.get_vendor(d['mac'])
            d['os'] = self.get_os(d['ttl']) if isinstance(d['ttl'], int) else "N/A"
            d['ports'] = self.scan_ports(d['ip'])
            self.results.append(d)
            self.root.after(0, self.update_ui, d, ((i+1)/total)*100)
        self.update_status(f"Escaneo finalizado. Gateway: {self.gateway_ip}")
        self.root.after(0, lambda: [self.scan_btn.config(state=tk.NORMAL), 
                                   self.export_btn.config(state=tk.NORMAL),
                                   self.graph_btn.config(state=tk.NORMAL)])

    def update_ui(self, d, progress):
        p_str = ", ".join(map(str, d['ports'])) if d['ports'] else "-"
        self.tree.insert("", tk.END, values=(d['ip'], d['mac'], d['vendor'], d['os'], p_str))
        self.progress_var.set(progress)

    def update_status(self, msg):
        self.root.after(0, lambda: self.status_label.config(text=msg))

    def show_topology(self):
        for widget in self.graph_tab.winfo_children(): widget.destroy()
        G = nx.Graph()
        scanner_node = "Scanner (Tú)"
        G.add_node(scanner_node, type='scanner')
        for d in self.results:
            label = f"{d['ip']}\n({d['os']})"
            node_type = 'gateway' if d['ip'] == self.gateway_ip else 'device'
            G.add_node(label, type=node_type)
            G.add_edge(scanner_node, label)
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)
        node_colors = []
        for node in G.nodes:
            ntype = G.nodes[node].get('type')
            if ntype == 'scanner': node_colors.append('red')
            elif ntype == 'gateway': node_colors.append('limegreen')
            else: node_colors.append('skyblue')
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, ax=ax)
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        ax.set_title("Topología Netwalk")
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=self.graph_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.notebook.select(self.graph_tab)

    def export_results(self):
        name = f"netwalk_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(f"{name}.json", "w") as j: json.dump(self.results, j, indent=4)
        messagebox.showinfo("Netwalk", f"Exportado como {name}.json")

if __name__ == "__main__":
    if is_admin():
        set_taskbar_icon()
        root = tk.Tk()
        app = NetwalkGUI(root)
        root.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)