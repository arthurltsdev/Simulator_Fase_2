from tkinter import Tk, Label, Button, Entry, StringVar, Frame, Listbox, END, Scrollbar, VERTICAL
from tkinter.messagebox import showinfo
from so.memory.memory_manager import MemoryManager
from so.so_pack.process import Process

class MemorySimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de memória - Paginação")
        # Memória de 256kb, página de 4kb
        self.memory_manager = MemoryManager(256, 4, self)

        self.init_process_size_input()
        self.init_process_buttons()
        self.init_memory_display()
        self.init_log_display()

    def init_log_display(self):
        self.log_frame = Frame(self.master)
        self.log_frame.pack(fill="both", expand=True)
        scrollbar = Scrollbar(self.log_frame, orient=VERTICAL)
        self.log_list = Listbox(self.log_frame, height=10, width=50, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_list.pack(side="left", fill="both", expand=True)
        Button(self.master, text="Limpar logs", command=self.clear_logs).pack()
        Button(self.master, text="Limpar memória", command=self.clear_memory).pack()

    def clear_logs(self):
        self.log_list.delete(0, END)

    def clear_memory(self):
        self.memory_manager.clear_memory()
        self.update_memory_display()

    def add_log(self, message):
        self.log_list.insert(END, message)
        self.log_list.see(END)

    def init_process_size_input(self):
        self.process_size_var = StringVar()
        Label(self.master, text="Tamanho do processo em kb:").pack()
        Entry(self.master, textvariable=self.process_size_var).pack()

    def init_process_buttons(self):
        Button(self.master, text="Adicionar Processo", command=self.add_process).pack()
        self.remove_process_id_var = StringVar()
        Entry(self.master, textvariable=self.remove_process_id_var, width=10).pack()
        Button(self.master, text="Remover Processo", command=self.remove_process).pack()

    def add_process(self):
        try:
            size = int(self.process_size_var.get())
            process = Process(size)
            added = self.memory_manager.write_using_paging(process)
            if added:
                showinfo("Successo!", f"Processo {process.id} adicionado com sucesso.")
            else:
                #self.add_log("Falha ao adicionar processo: Memória Insuficiente ou Page Fault")
                #O log foi adicionado na função write_using_paging do arquivo memory_manager.py
                pass
            self.update_memory_display()
        except ValueError:
            showinfo("Erro", "Tamanho do processo inválido.")

    def remove_process(self):
        process_id = self.remove_process_id_var.get().upper()
        process = Process(0)
        process.id = process_id
        removed = self.memory_manager.delete(process)
        if removed:
            showinfo("Successo", f"Processo {process_id} removido com sucesso.")
        else:
            self.add_log(f"Processo {process_id} não encontrado para remoção")
        self.update_memory_display()

    def init_memory_display(self):
        self.memory_frame = Frame(self.master)
        self.memory_frame.pack()
        self.memory_labels = []
        # Para uma memória de 256kb e páginas de 4kb, o total de 64 páginas serão divididas 4 linhas de 16 colunas para melhor visualização.
        columns = 16
        for i in range(self.memory_manager.pages):
            row = i // columns
            column = i % columns
            lbl = Label(self.memory_frame, text="", bg="white", width=2, height=1, borderwidth=1, relief="solid")
            lbl.grid(row=row, column=column)
            self.memory_labels.append(lbl)
        self.update_memory_display()

    def update_memory_display(self):
        for i, lbl in enumerate(self.memory_labels):
            page_index = i
            page_content = [self.memory_manager.physicalMemory[page_index][sub_index] for sub_index in range(self.memory_manager.pageSize)]
            if any(content is not None for content in page_content):
                lbl.config(text=page_content[0], bg="green")
            else:
                lbl.config(text="", bg="white")

if __name__ == "__main__":
    root = Tk()
    gui = MemorySimulatorGUI(root)
    root.mainloop()