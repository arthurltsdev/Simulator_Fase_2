from so.memory.strategy import Strategy
from so.memory.address_memory import AddressMemory

class MemoryManager:
    def __init__(self, memory_size: int = 128, default_strategy=Strategy.FIRST_FIT):
        self.strategy = default_strategy
        self.memory_size = memory_size
        self.memory = [None] * memory_size
        self.allocated_processes = {}

    def set_strategy(self, strategy):
        self.strategy = strategy

    def allocate(self, process_id, size_in_memory):
        if self.strategy == Strategy.FIRST_FIT:
            return self.allocate_using_first_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.BEST_FIT:
            return self.allocate_using_best_fit(process_id, size_in_memory)
        elif self.strategy == Strategy.WORST_FIT:
            return self.allocate_using_worst_fit(process_id, size_in_memory)
        return False

    def deallocate(self, process_id):
        if process_id in self.allocated_processes:
            address_memory = self.allocated_processes.pop(process_id)
            for i in range(address_memory.start, address_memory.end + 1):
                self.memory[i] = None
            return True
        return False

    def allocate_using_first_fit(self, process_id, size_in_memory):
        for i in range(len(self.memory) - size_in_memory + 1):
            if all(self.memory[j] is None for j in range(i, i + size_in_memory)):
                for j in range(i, i + size_in_memory):
                    self.memory[j] = process_id
                self.allocated_processes[process_id] = AddressMemory(i, i + size_in_memory - 1)
                return True
        return False

    def allocate_using_best_fit(self, process_id, size_in_memory):
        best_fit_index = -1
        best_fit_size = float('inf')
        for i in range(len(self.memory) - size_in_memory + 1):
            if all(self.memory[j] is None for j in range(i, i + size_in_memory)):
                current_fit_size = 0
                for j in range(i + size_in_memory, len(self.memory)):
                    if self.memory[j] is None:
                        current_fit_size += 1
                    else:
                        break
                if current_fit_size < best_fit_size:
                    best_fit_index, best_fit_size = i, current_fit_size
        if best_fit_index != -1:
            for i in range(best_fit_index, best_fit_index + size_in_memory):
                self.memory[i] = process_id
            self.allocated_processes[process_id] = AddressMemory(best_fit_index, best_fit_index + size_in_memory - 1)
            return True
        return False

    def allocate_using_worst_fit(self, process_id, size_in_memory):
        worst_fit_index = -1
        worst_fit_size = 0
        for i in range(len(self.memory) - size_in_memory + 1):
            if all(self.memory[j] is None for j in range(i, i + size_in_memory)):
                current_fit_size = 0
                for j in range(i + size_in_memory, len(self.memory)):
                    if self.memory[j] is None:
                        current_fit_size += 1
                    else:
                        break
                if current_fit_size > worst_fit_size:
                    worst_fit_index, worst_fit_size = i, current_fit_size
        if worst_fit_index != -1:
            for i in range(worst_fit_index, worst_fit_index + size_in_memory):
                self.memory[i] = process_id
            self.allocated_processes[process_id] = AddressMemory(worst_fit_index, worst_fit_index + size_in_memory - 1)
            return True
        return False

