# ui/layout.py
import customtkinter as ctk
from tkinter import filedialog
import json
from ui.eventos import alternar_tema, toggle_dropdown, atualizar_botao_setores, analisar

# === Carregamento de dados globais ===
with open("data/setores.json", "r", encoding="utf-8") as f:
    SETORES = json.load(f)

with open("data/enterprises_name.json", "r", encoding="utf-8") as f:
    NOMES_EMPRESAS = json.load(f)

def iniciar_app():
    app = ctk.CTk()
    app.title("📊 StocksTracker")
    app.geometry("750x600")
    check_vars = {}
    indicadores_vars = {
        "SMA": ctk.BooleanVar(value=True),
        "EMA": ctk.BooleanVar(value=True),
        "RSI": ctk.BooleanVar(value=False),
         "IA": ctk.BooleanVar(value=True)
    }

    scroll_frame = ctk.CTkScrollableFrame(app, corner_radius=20, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    top_frame = ctk.CTkFrame(scroll_frame, corner_radius=15)
    top_frame.pack(pady=10, padx=20, fill='x')

    titulo = ctk.CTkLabel(top_frame, text="📈 StocksTracker", font=ctk.CTkFont(size=22, weight="bold"))
    titulo.pack(side="left", padx=15, pady=10)

    tema_switch = ctk.CTkSwitch(top_frame, text="Modo Claro")
    tema_switch.configure(command=lambda: alternar_tema(tema_switch))
    tema_switch.pack(side="right", padx=15)

    ctk.CTkLabel(scroll_frame, text="Gere um PDF com a variação dos setores econômicos nas últimas semanas", font=ctk.CTkFont(size=14), justify="center").pack(pady=10)

    main_frame = ctk.CTkFrame(scroll_frame, corner_radius=15)
    main_frame.pack(pady=10, padx=20)

    ctk.CTkLabel(main_frame, text="📂 Setores:").grid(row=0, column=0, padx=5, pady=5, sticky='ne')
    dropdown_container = ctk.CTkFrame(main_frame, fg_color=main_frame.cget("fg_color"))
    dropdown_container.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

    dropdown_frame = ctk.CTkFrame(dropdown_container, fg_color=main_frame.cget("fg_color"))
    empresa_label = ctk.CTkLabel(dropdown_frame, text="Total de empresas selecionadas: 0", anchor='w', font=ctk.CTkFont(size=13, weight="bold"))
    empresa_label.pack(anchor='w', padx=10, pady=(5, 5))
    dropdown_frame.pack_forget()

    setores_btn = ctk.CTkButton(dropdown_container, text="Selecionar Setores",
        command=lambda: toggle_dropdown(dropdown_frame, dropdown_container, empresa_label))
    setores_btn.pack(anchor='w')

    for setor in SETORES:
        var = ctk.BooleanVar()
        var.trace_add("write", lambda *_, v=var: atualizar_botao_setores(check_vars, SETORES, setores_btn, empresa_label))
        chk = ctk.CTkCheckBox(dropdown_frame, text=setor, variable=var)
        chk.pack(anchor='w', padx=10)
        check_vars[setor] = var

    ctk.CTkLabel(main_frame, text="📅 Dias:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_dias = ctk.CTkEntry(main_frame, width=100)
    entry_dias.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    indicadores_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color="transparent")
    indicadores_frame.pack(pady=(5, 10))

    linha_indicadores = ctk.CTkFrame(indicadores_frame, fg_color="transparent")
    linha_indicadores.pack(anchor='center', padx=10, pady=10)

    ctk.CTkLabel(linha_indicadores, text="📈 Indicadores Técnicos:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
    for nome, var in indicadores_vars.items():
        chk = ctk.CTkCheckBox(linha_indicadores, text=nome, variable=var)
        chk.pack(side="left", padx=8)

    ctk.CTkLabel(scroll_frame, text="📀 Escolha uma pasta para salvar o PDF:").pack(pady=(10, 0))
    frame_pasta = ctk.CTkFrame(scroll_frame)
    frame_pasta.pack(pady=5)

    entry_pasta = ctk.CTkEntry(frame_pasta, width=400)
    entry_pasta.pack(side="left", padx=5)

    btn_browse = ctk.CTkButton(frame_pasta, text="📁 Browse", command=lambda: entry_pasta.insert(0, filedialog.askdirectory()))
    btn_browse.pack(side="left")

    progress = ctk.CTkProgressBar(scroll_frame, width=400)
    progress.set(0)
    progress.pack(pady=(5, 10))

    status_label = ctk.CTkLabel(scroll_frame, text="")
    status_label.pack()

    btn_analisar = ctk.CTkButton(scroll_frame, text="✔ Analisar",
        command=lambda: analisar(check_vars, entry_dias, entry_pasta, SETORES, NOMES_EMPRESAS, indicadores_vars, btn_analisar, progress, status_label))
    btn_analisar.pack(pady=(10, 5))

    def fechar_dropdown(event):
        if not dropdown_frame.winfo_containing(event.x_root, event.y_root):
            dropdown_frame.pack_forget()

    app.bind('<Button-1>', fechar_dropdown)
    app.mainloop()
