from tkinter import Tk, Label, Button, Entry, StringVar, Frame, Listbox, END, Scrollbar, VERTICAL, OptionMenu
from tkinter.messagebox import showinfo
import threading
from so.memory.memory_manager import MemoryManager
from so.so_pack.process import Process
from so.cpu.cpu_manager import CPUManager


class MemorySimulatorGUI:
    def __init__(self, master):
        self.remove_process_id_var = None
        self.master = master
        self.master.title("Simulador de memória e CPU - Escalonamento")
        self.cpu_manager = CPUManager(self)  # Passa a própria GUI como parâmetro para logs
        self.memory_manager = MemoryManager(256, 1, self)
        self.priority_var = StringVar(value="Média")  # Valor padrão
        self.algorithm_var = StringVar(value=None)
        self.init_priority_selection()
        self.init_algorithm_selection()
        self.init_process_size_input()
        self.init_process_buttons()
        self.init_memory_display()
        self.init_log_display()


    def init_priority_selection(self):
        priorities = ["Baixa", "Média", "Crítica"]
        Label(self.master, text="Defina a prioridade:").pack()
        OptionMenu(self.master, self.priority_var, *priorities).pack()

    def add_to_queue(self):
        size = int(self.process_size_var.get())
        priority = self.priority_var.get()
        process = Process(size, priority)
        self.cpu_manager.add_process(process)
        self.log_list.insert(END, f"Processo {process.id} com prioridade {priority} e tamanho {size} adicionado à fila de CPU.")

    def init_algorithm_selection(self):
        Label(self.master, text="Escolha um algoritmo:").pack()
        algorithms = ["FCFS", "Lottery", "Priority", "SJF"]
        self.algorithm_var = StringVar(value="Selecione um algoritmo")  # Valor inicial
        alg_menu = OptionMenu(self.master, self.algorithm_var, *algorithms, command=self.update_algorithm)
        alg_menu.pack()

    def update_algorithm(self, choice):
        self.cpu_manager.set_algorithm(choice)
        self.add_log(f"Algoritmo de escalonamento definido para: {choice}")

    def init_process_buttons(self):
        Button(self.master, text="Adicionar à fila", command=self.add_to_queue).pack()
        Button(self.master, text="Executar", command=self.execute).pack()
        self.init_remove_process_button()

    def init_remove_process_button(self):
        # Campo de entrada para o ID do processo a ser removido
        self.remove_process_id_var = StringVar()
        Label(self.master, text="Digite o ID do Processo para remover:").pack()
        Entry(self.master, textvariable=self.remove_process_id_var).pack()

        # Botão para remover o processo
        remove_button = Button(self.master, text="Remover Processo", command=self.remove_process)
        remove_button.pack()

    def init_log_display(self):
        self.log_frame = Frame(self.master)
        self.log_frame.pack(fill="both", expand=True)
        scrollbar = Scrollbar(self.log_frame, orient=VERTICAL)
        self.log_list = Listbox(self.log_frame, height=10, width=50, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_list.pack(side="left", fill="both", expand=True)
        Button(self.master, text="Limpar logs", command=self.clear_logs).pack()


    def clear_logs(self):
        self.log_list.delete(0, END)


    def add_log(self, message):
        self.log_list.insert(END, message)
        self.log_list.see(END)

    def init_process_size_input(self):
        self.process_size_var = StringVar()
        Label(self.master, text="Tamanho do processo em kb:").pack()
        Entry(self.master, textvariable=self.process_size_var).pack()


    def execute(self):
        if not self.algorithm_var.get() or self.algorithm_var.get() == "Escolha um algoritmo":
            self.add_log("Por favor, escolha um algoritmo de escalonamento antes de executar.")
        else:
            self.cpu_manager.set_algorithm(self.algorithm_var.get())
            thread = threading.Thread(target=self.cpu_manager.run)
            thread.start()

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
        removed = self.memory_manager.delete(process_id)
        if removed:
            showinfo("Successo", f"Processo {process_id} removido com sucesso.")
        else:
            self.add_log(f"Processo {process_id} não encontrado para remoção")
        self.update_memory_display()

    def init_memory_display(self):
        self.memory_frame = Frame(self.master)
        self.memory_frame.pack(expand=True, fill='both')
        self.memory_labels = []
        rows = 16
        columns = 32  # Configuring for 256 frames in a 16x16 grid

        for i in range(256):
            lbl = Label(self.memory_frame, text="", bg="white", width=5, height=1, relief="solid")
            lbl.grid(row=i // columns, column=i % columns, padx=1, pady=1)
            self.memory_labels.append(lbl)

    def update_memory_display(self):
        for i, lbl in enumerate(self.memory_labels):
            frame_content = self.memory_manager.physicalMemory[i][0]
            if frame_content:
                lbl.config(text=frame_content.id, bg='green')
            else:
                lbl.config(text="", bg='white')


if __name__ == "__main__":
    root = Tk()
    gui = MemorySimulatorGUI(root)
    root.mainloop()