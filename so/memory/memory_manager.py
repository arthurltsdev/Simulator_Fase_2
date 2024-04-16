from so.memory.frame_memory import FrameMemory

class MemoryManager:
    def __init__(self, memorySize, pageSize, gui=None):
        self.pageSize = pageSize
        self.memorySize = memorySize
        self.pages = (self.memorySize + self.pageSize - 1) // self.pageSize
        self.physicalMemory = [[None] * self.pageSize for _ in range(self.pages)]
        self.logicalMemory = {}
        self.gui = gui

    def write_using_paging(self, process):
        frames = self.get_frames(process)
        if not frames:
            if self.gui:
                self.gui.add_log("Page Fault: Não há memória disponível para alocar o processo.")
            return False
        for frame in frames:
            start_index = frame.get_page_num() * self.pageSize
            end_index = start_index + self.pageSize
            for j in range(start_index, end_index):
                page_index = j // self.pageSize
                sub_index = j % self.pageSize
                self.physicalMemory[page_index][sub_index] = process.id
        self.logicalMemory[process.id] = frames
        # Calcula a memória restante para printar o log a cada novo processo adicionado
        remaining_pages = sum(1 for frame in self.physicalMemory if frame[0] is None)
        remaining_memory_kb = remaining_pages * self.pageSize
        if self.gui:
            self.gui.add_log(f"Espaço restante em memória: {remaining_memory_kb} kb.")
        # Verifica se a memória está completamente cheia e loga se estiver
        if all(frame[0] is not None for frame in self.physicalMemory):
            if self.gui:
                self.gui.add_log("Memória completamente cheia.")

        return True

    def get_frames(self, process):
        frames = []
        actuallyProcessSize = 0
        for frame in range(self.pages):
            if self.physicalMemory[frame][0] is None:
                frames.append(FrameMemory(frame, self.pageSize))
                actuallyProcessSize += self.pageSize
                if actuallyProcessSize >= process.sizeInMemory:
                    return frames
        if actuallyProcessSize < process.sizeInMemory:
            # Retorna lista vazia se não houver espaço suficiente
            return []
        return frames

    def delete(self, process):
        if process.id in self.logicalMemory:
            frames = self.logicalMemory[process.id]
            for frame in frames:
                start_index = frame.get_page_num() * self.pageSize
                end_index = start_index + self.pageSize
                for j in range(start_index, end_index):
                    page_index = j // self.pageSize
                    sub_index = j % self.pageSize
                    self.physicalMemory[page_index][sub_index] = None
            del self.logicalMemory[process.id]
            return True
        if self.gui:
            self.gui.add_log(f"Processo {process.id} não encontrado.")
        return False

    def clear_memory(self):
        self.physicalMemory = [[None] * self.pageSize for _ in range(self.pages)]
        self.logicalMemory = {}
        if self.gui:
            self.gui.add_log("Todos os processos foram removidos.")

