from so.so_pack.subprocess import SubProcess


class Process:
    count = 0

    def __init__(self, size):
        Process.count += 1
        self.id = f"P{Process.count}"
        self.sizeInMemory = size
        self.subProcesses = []

    def get_sub_processes(self):
        if not self.subProcesses:
            for i in range(self.sizeInMemory):
                self.subProcesses.append(SubProcess(self.id, 7))
        return self.subProcesses
