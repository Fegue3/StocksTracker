# ui/eventos.py
import customtkinter as ctk
from tkinter import messagebox
import threading
from core.pdf_generator import gerar_pdf

def alternar_tema(switch):
    modo = "light" if switch.get() == 1 else "dark"
    switch.configure(text="Modo Escuro" if modo == "light" else "Modo Claro")
    ctk.set_appearance_mode(modo)

def toggle_dropdown(dropdown_frame, dropdown_container, empresa_label):
    if dropdown_frame.winfo_ismapped():
        dropdown_frame.pack_forget()
    else:
        dropdown_frame.configure(fg_color=dropdown_container.cget("fg_color"))
        dropdown_frame.pack(pady=(5, 0), anchor='w')
        empresa_label.pack(anchor='w', pady=(5, 5))

def atualizar_botao_setores(check_vars, SETORES, setores_btn, empresa_label):
    count = sum(var.get() for var in check_vars.values())
    texto = f"Selecionar Setores ({count})" if count else "Selecionar Setores"
    setores_btn.configure(text=texto)
    total_empresas = sum(len(SETORES[setor]) for setor, var in check_vars.items() if var.get())
    empresa_label.configure(text=f"Total de empresas selecionadas: {total_empresas}")

def analisar(check_vars, entry_dias, entry_pasta, SETORES, NOMES_EMPRESAS, indicadores_vars, btn_analisar, progress, status_label):
    setores_selecionados = [setor for setor, var in check_vars.items() if var.get()]
    dias = entry_dias.get()
    pasta = entry_pasta.get()

    if not setores_selecionados or not dias or not pasta:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    try:
        dias = int(dias)
    except ValueError:
        messagebox.showwarning("Valor inválido", "O campo 'dias' deve ser um número inteiro!")
        return

    def callback_ui(status, msg=None):
        if status == 'start':
            btn_analisar.configure(state="disabled")
            progress.set(0)
            status_label.configure(text="Iniciando análise...")
        elif status == 'processing':
            status_label.configure(text=f"Processando: {msg}")
        elif status == 'done':
            progress.set(100)
            status_label.configure(text="Análise concluída!")
            messagebox.showinfo("Sucesso", f"PDF salvo em:\n{msg}")
            btn_analisar.configure(state="normal")
        elif status == 'error':
            messagebox.showerror("Erro ao gerar PDF", msg)
            status_label.configure(text="Erro durante análise")
            btn_analisar.configure(state="normal")

    threading.Thread(
        target=gerar_pdf,
        args=(setores_selecionados, dias, pasta, SETORES, NOMES_EMPRESAS, indicadores_vars, callback_ui),
        daemon=True
    ).start()
