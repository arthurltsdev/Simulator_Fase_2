from so.memory.strategy import Strategy
from so.so_pack import process
class MemoryManager:
    def __init__(self, memory_size: int = 128, default_strategy=Strategy.PAGING):
        self.strategy = default_strategy
        self.physicalMemory = [None] * 128  # Simulando a memória física com 128 posições
        self.logicalMemory = {}  # Dicionário para simular a Hashtable do Java

    def add_process_to_logical_memory(self, process_id, frame_memory):
        if process_id not in self.logicalMemory:
            self.logicalMemory[process_id] = []
        self.logicalMemory[process_id].append(frame_memory)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def allocate(self, process_id):
        if self.strategy == Strategy.FIRST_FIT:
            return self.allocate_using_first_fit(process_id)
        elif self.strategy == Strategy.BEST_FIT:
            return self.allocate_using_best_fit(process_id)
        elif self.strategy == Strategy.WORST_FIT:
            return self.allocate_using_worst_fit(process_id)
        elif self.strategy == Strategy.PAGING:
            return self.allocate_using_paging(process_id)
        return False

    def allocate_using_paging(process_id):

    def delete(process_id):
        for




