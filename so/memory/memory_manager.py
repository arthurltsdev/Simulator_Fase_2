from so.memory.frame_memory import FrameMemory


class MemoryManager:
    def __init__(self, memorySize, pageSize, gui=None):
        self.pageSize = pageSize  # Cada página pode conter 1 subprocesso (assumindo que 1 unidade de tamanho é equivalente a 1 subprocesso)
        self.memorySize = memorySize
        self.pages = (self.memorySize + self.pageSize - 1) // self.pageSize
        self.physicalMemory = [[None] * self.pageSize for _ in range(self.pages)]
        self.logicalMemory = {}
        self.gui = gui

    def write_using_paging(self, process):
        sub_processes = process.get_sub_processes()
        if not sub_processes:
            if self.gui:
                self.gui.add_log("Falha: Nenhum subprocesso para alocar.")
            return False

        frames = self.get_frames(len(sub_processes))
        if not frames:
            if self.gui:
                self.gui.add_log("Page Fault: Não há memória disponível para alocar o processo.")
            return False

        for frame, sp in zip(frames, sub_processes):
            self.physicalMemory[frame.page_num][0] = sp  # Alocando cada subprocesso em uma página
            self.logicalMemory[sp.id] = frame

        remaining_pages = sum(1 for frame in self.physicalMemory if frame[0] is None)
        remaining_memory_kb = remaining_pages * self.pageSize
        if self.gui:
            self.gui.add_log(f"Espaço restante em memória: {remaining_memory_kb} kb.")

        if all(frame[0] is not None for frame in self.physicalMemory):
            if self.gui:
                self.gui.add_log("Memória completamente cheia.")
        return True

    def get_frames(self, num_subprocesses):
        frames = []
        for i, frame in enumerate(self.physicalMemory):
            if frame[0] is None:
                frames.append(FrameMemory(i, 0))
                if len(frames) == num_subprocesses:
                    return frames
        return []

    def delete(self, process_id):
        # Removendo subprocessos da memória física baseado no process_id
        removed = False
        for page in self.physicalMemory:
            for i, sp in enumerate(page):
                if sp is not None and sp.id.startswith(process_id):
                    page[i] = None  # Limpa o frame que contém o subprocesso
                    removed = True

        if removed:
            self.gui.add_log(f"Processo {process_id} removido com sucesso.")
        else:
            self.gui.add_log(f"Processo {process_id} não encontrado.")
        return removed

