from tkinter import Tk, Label, Button, Entry, StringVar, Frame
from tkinter.messagebox import showinfo
from so.memory.memory_manager import MemoryManager
from so.so_pack.process import Process

class MemorySimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de memória - Paginação")
        #Inicializando o Memory Manager com uma memória de 256kb e cada página de tamanho 4kb.
        self.memory_manager = MemoryManager(256, 4)

        self.init_process_size_input()
        self.init_process_buttons()
        self.init_memory_display()

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
            self.memory_manager.write_using_paging(process)
            showinfo("Successo!", f"Processo {process.id} adicionado com sucesso.")
            self.update_memory_display()
        except ValueError:
            showinfo("Erro", "Tamanho do processo inválido.")

    def remove_process(self):
        process_id = self.remove_process_id_var.get().upper()
        process = Process(0)  # Inicializa para deletar em seguida
        process.id = process_id
        self.memory_manager.delete(process)
        showinfo("Successo", f"Processo {process_id} removido com sucesso.")
        self.update_memory_display()

    def init_memory_display(self):
        self.memory_frame = Frame(self.master)
        self.memory_frame.pack()
        self.memory_labels = []
        columns = 16  # Como são 64 páginas, serão divididas em 16 colunas e 4 linhas para melhor visualização.
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