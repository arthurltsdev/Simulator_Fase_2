from so.memory.frame_memory import FrameMemory

class MemoryManager:
    def __init__(self, memorySize, pageSize):
        self.pageSize = pageSize
        self.memorySize = memorySize
        self.pages = (self.memorySize + self.pageSize - 1) // self.pageSize
        self.physicalMemory = [[None] * self.pageSize for _ in range(self.pages)]
        self.logicalMemory = {}

    def write_using_paging(self, process):
        frames = self.get_frames(process)
        total_units_to_allocate = process.sizeInMemory
        for frame in frames:
            if total_units_to_allocate <= 0:
                break
            units_to_allocate = min(self.pageSize, total_units_to_allocate)
            start_index = frame.get_page_num() * self.pageSize
            end_index = start_index + units_to_allocate
            for j in range(start_index, end_index):
                page_index = j // self.pageSize
                sub_index = j % self.pageSize
                self.physicalMemory[page_index][sub_index] = process.id
            total_units_to_allocate -= units_to_allocate
        self.logicalMemory[process.id] = frames

    def get_frames(self, process):
        frames = []
        actuallyProcessSize = 0
        for frame in range(self.pages):
            if self.physicalMemory[frame][0] is None:
                frames.append(FrameMemory(frame, self.pageSize))
                actuallyProcessSize += self.pageSize
                if actuallyProcessSize >= process.sizeInMemory:
                    break
        return frames

    def delete(self, process):
        if process.id in self.logicalMemory:
            frames = self.logicalMemory[process.id]
            for frame in frames:
                start_index = frame.get_page_num() * self.pageSize
                end_index = start_index + self.pageSize
                # Garantindo que cada unidade dentro do frame seja removida
                for j in range(start_index, end_index):
                    page_index = j // self.pageSize
                    sub_index = j % self.pageSize
                    self.physicalMemory[page_index][sub_index] = None
            # Remova a entrada do dicionário após limpar todos os frames
            del self.logicalMemory[process.id]
        else:
            print(f"Process {process.id} not found in memory.")

