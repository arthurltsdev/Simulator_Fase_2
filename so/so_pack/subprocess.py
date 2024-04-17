class SubProcess:
    count = 0
    last_process_id = None

    def __init__(self, process_id, instructions):
        if process_id != SubProcess.last_process_id:
            SubProcess.count = 0
            SubProcess.last_process_id = process_id
        SubProcess.count += 1
        self.id = f"{process_id} S{SubProcess.count}"
        self.instructions = instructions
