import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import ipaddress
import json
import os

DATA_FILE = "routini_data.json"

def save_to_json(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_from_json():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def get_commands(name, ip_input, net_input, r_type):
    try:
        is_ipv6 = ":" in ip_input
        res = f"\n! --- CONFIGURACIÓN {'IPv6' if is_ipv6 else 'IPv4'}: {name} ---\n"
        
        # Validar y procesar máscara/prefijo
        mask_val = net_input.strip()
        if not is_ipv6:
            # Soporta tanto "24" como "255.255.255.0"
            net = ipaddress.IPv4Network(f"{ip_input}/{mask_val}", strict=False)
            mask = net.netmask
            network_addr = net.network_address
            
            if r_type == "Interfaz/Alias":
                res += f"interface [INTERFAZ]\n description {name}\n ip address {ip_input} {mask}\n no shutdown\n"
            elif r_type == "Estático":
                res += f"ip route {network_addr} {mask} [SIGUIENTE_SALTO]\n"
            elif r_type == "OSPF":
                res += f"router ospf 1\n network {network_addr} area 0\n"
            elif r_type == "EIGRP":
                res += f"router eigrp 1\n network {network_addr}\n no auto-summary\n"
        else:
            net = ipaddress.IPv6Network(f"{ip_input}/{mask_val}", strict=False)
            network_addr, prefix = net.network_address, net.prefixlen
            if r_type == "Interfaz/Alias":
                res += f"ipv6 unicast-routing\ninterface [INTERFAZ]\n description {name}\n ipv6 address {ip_input}/{prefix}\n no shutdown\n"
            elif r_type == "Estático":
                res += f"ipv6 route {network_addr}/{prefix} [SIGUIENTE_SALTO]\n"
            elif r_type == "OSPF":
                res += f"ipv6 router ospf 1\n router-id 1.1.1.1\n!\ninterface [INTERFAZ]\n ipv6 ospf 1 area 0\n"
            elif r_type == "EIGRP":
                res += f"ipv6 router eigrp 1\n eigrp router-id 1.1.1.1\n no shutdown\n"
        return res
    except Exception as e:
        return f"! Error en {name}: {e}\n"

def add_entry():
    router = entry_router.get()
    name = entry_name.get()
    ip = entry_ip.get()
    mask = entry_net.get()
    rtype = combo_type.get()
    if all([router, name, ip, mask, rtype]):
        tree.insert("", "end", values=(router, name, ip, mask, rtype))
        save_current_list()
        entry_name.delete(0, tk.END)
        entry_ip.delete(0, tk.END)
        entry_net.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Complete todos los campos.")

def save_current_list():
    data = [tree.item(i)['values'] for i in tree.get_children()]
    save_to_json(data)

def delete_entry():
    selected = tree.selection()
    for item in selected:
        tree.delete(item)
    save_current_list()

def generate_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Seleccione al menos una red.")
        return
    output_text.delete(1.0, tk.END)
    for item in selected:
        val = tree.item(item)['values']
        output_text.insert(tk.END, f"! ROUTER: {val[0]}\n" + get_commands(val[1], val[2], val[3], val[4]))

def generate_all():
    output_text.delete(1.0, tk.END)
    for item in tree.get_children():
        val = tree.item(item)['values']
        output_text.insert(tk.END, f"! ROUTER: {val[0]}\n" + get_commands(val[1], val[2], val[3], val[4]))

def copy_text():
    content = output_text.get(1.0, tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")

# --- INTERFAZ ---
root = tk.Tk()
root.title("Routini")
root.geometry("800x900")
try: root.iconbitmap('routini.ico')
except: pass

# Nota de instrucciones
note_text = ("PASOS A SEGUIR:\n"
             "1. Ingrese el nombre del Router (ej: R1) y de la Red (ej: LAN_Ventas).\n"
             "2. Ingrese IP y Máscara (Ejemplos: 192.168.1.0 con 24 O 255.255.255.0).\n"
             "3. Click en 'AGREGAR RED' para guardar en la lista.\n"
             "4. Seleccione redes de la tabla y click en 'GENERAR' para ver los comandos.")

lbl_note = tk.Label(root, text=note_text, fg="red", font=('Arial', 9, 'bold'), justify="left", wraplength=700)
lbl_note.pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack(pady=5)

fields = [("Router:", entry_router := tk.Entry(frame_input, width=35)),
          ("Nombre Red:", entry_name := tk.Entry(frame_input, width=35)),
          ("IP:", entry_ip := tk.Entry(frame_input, width=35)),
          ("Máscara/Prefijo:", entry_net := tk.Entry(frame_input, width=35))]

for i, (label, entry) in enumerate(fields):
    tk.Label(frame_input, text=label, font=('Arial', 9, 'bold')).grid(row=i, column=0, sticky="e", padx=5)
    entry.grid(row=i, column=1, pady=2)

tk.Label(frame_input, text="Tipo:", font=('Arial', 9, 'bold')).grid(row=4, column=0, sticky="e", padx=5)
combo_type = ttk.Combobox(frame_input, values=["Interfaz/Alias", "Estático", "OSPF", "EIGRP"], state="readonly", width=32)
combo_type.grid(row=4, column=1, pady=2)
combo_type.current(0)

tk.Button(frame_input, text="AGREGAR RED", command=add_entry, bg="#3498db", fg="white", font=('Arial', 9, 'bold'), width=25).grid(row=5, column=0, columnspan=2, pady=10)

tree = ttk.Treeview(root, columns=("Router", "Nombre", "IP", "Máscara", "Tipo"), show='headings', height=10)
for col in ("Router", "Nombre", "IP", "Máscara", "Tipo"):
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack(pady=10, padx=10, fill="x")

# Cargar datos previos
for row in load_from_json(): tree.insert("", "end", values=row)

frame_btns = tk.Frame(root)
frame_btns.pack(pady=5)
tk.Button(frame_btns, text="BORRAR SELECCIONADO", command=delete_entry, bg="#e74c3c", fg="white", font=('Arial', 8, 'bold')).pack(side="left", padx=5)
tk.Button(frame_btns, text="GENERAR SELECCIONADO", command=generate_selected, bg="#2c3e50", fg="white", font=('Arial', 8, 'bold')).pack(side="left", padx=5)
tk.Button(frame_btns, text="GENERAR TODO", command=generate_all, bg="#2c3e50", fg="white", font=('Arial', 8, 'bold')).pack(side="left", padx=5)
tk.Button(frame_btns, text="COPIAR RESULTADO", command=copy_text, bg="#27ae60", fg="white", font=('Arial', 8, 'bold')).pack(side="left", padx=5)

output_text = scrolledtext.ScrolledText(root, width=90, height=20, font=('Consolas', 10))
output_text.pack(pady=10, padx=10)

root.mainloop()