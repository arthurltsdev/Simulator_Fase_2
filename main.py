from tkinter import Tk, Label, Button, Entry, StringVar, Radiobutton, Frame
from tkinter.messagebox import showinfo
from so.memory.memory_manager import MemoryManager
from so.memory.strategy import Strategy
from so.so_pack.process import Process

# Initialize the GUI application for the Memory Simulator
class MemorySimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Simulator")

        # Initialize Memory Manager with First Fit strategy and 128 memory units
        self.memory_manager = MemoryManager(128, Strategy.FIRST_FIT)

        # Strategy selection
        self.strategy_var = StringVar(value="1")
        self.init_strategy_selection()

        # Process size input
        self.init_process_size_input()

        # Add and Remove process buttons
        self.init_process_buttons()

        # Memory state display
        self.init_memory_display()

    def init_strategy_selection(self):
        Label(self.master, text="Select Allocation Strategy:").pack()
        strategies = {"First Fit": "1", "Best Fit": "2", "Worst Fit": "3"}
        for text, value in strategies.items():
            Radiobutton(self.master, text=text, variable=self.strategy_var, value=value, command=self.change_strategy).pack()

    def change_strategy(self):
        strategy = int(self.strategy_var.get())
        if strategy == 1:
            self.memory_manager.set_strategy(Strategy.FIRST_FIT)
        elif strategy == 2:
            self.memory_manager.set_strategy(Strategy.BEST_FIT)
        elif strategy == 3:
            self.memory_manager.set_strategy(Strategy.WORST_FIT)
        self.update_memory_display()

    def init_process_size_input(self):
        self.process_size_var = StringVar()
        Label(self.master, text="Process Size:").pack()
        Entry(self.master, textvariable=self.process_size_var).pack()

    def init_process_buttons(self):
        Button(self.master, text="Add Process", command=self.add_process).pack()
        self.remove_process_id_var = StringVar()
        Entry(self.master, textvariable=self.remove_process_id_var, width=10).pack()
        Button(self.master, text="Remove Process", command=self.remove_process).pack()

    def add_process(self):
        try:
            size = int(self.process_size_var.get())
            process = Process(size)
            success = self.memory_manager.allocate(process.get_id(), process.get_size_in_memory())
            if success:
                showinfo("Success", f"Process {process.get_id()} added.")
            else:
                showinfo("Error", "Failed to add process.")
            self.update_memory_display()
        except ValueError:
            showinfo("Error", "Invalid process size.")

    def remove_process(self):
        process_id = self.remove_process_id_var.get().upper()
        success = self.memory_manager.deallocate(process_id)
        if success:
            showinfo("Success", f"Process {process_id} removed.")
        else:
            showinfo("Error", f"Process {process_id} not found.")
        self.update_memory_display()

    def init_memory_display(self):
        self.memory_frame = Frame(self.master)
        self.memory_frame.pack()
        self.memory_labels = []
        # Define the number of columns in the grid
        columns = 16  # This will result in 8 rows for 128 memory blocks
        for i in range(self.memory_manager.memory_size):
            row = i // columns
            column = i % columns
            lbl = Label(self.memory_frame, text="", bg="white", width=2, borderwidth=1, relief="solid")
            lbl.grid(row=row, column=column)
            self.memory_labels.append(lbl)
        self.update_memory_display()

    def update_memory_display(self):
        for i, lbl in enumerate(self.memory_labels):
            process_id = self.memory_manager.memory[i]
            lbl.config(text=process_id if process_id else "", bg="green" if process_id else "white")

if __name__ == "__main__":
    root = Tk()
    gui = MemorySimulatorGUI(root)
    root.mainloop()

