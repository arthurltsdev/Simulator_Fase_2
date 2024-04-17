from so.so_pack.subprocess import SubProcess

class Process:
    count = 0

    def __init__(self, size):
        Process.count += 1
        self.id = f"P{Process.count}"
        self.sizeInMemory = size
        self.subProcesses = self.create_sub_processes()

    def create_sub_processes(self):
        sub_processes = []
        for _ in range(self.sizeInMemory):  # Cada unidade de size representa um subprocesso
            sub_processes.append(SubProcess(self.id, 7))
        return sub_processes

    def get_sub_processes(self):
        return self.subProcesses
