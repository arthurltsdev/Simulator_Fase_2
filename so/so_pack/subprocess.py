class SubProcess:
    count = 0

    def __init__(self, processId, instructions):
        SubProcess.count += 1
        self.id = f"{processId}{SubProcess.count}"
        self.instructions = instructions
