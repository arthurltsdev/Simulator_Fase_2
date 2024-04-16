class SystemOperation:
    cm = None
    mm = None

    @staticmethod
    def system_call(type, arg):
        if type == "WRITE_PROCESS":
            if SystemOperation.cm is None:
                SystemOperation.cm = CpuManager()  # Assuming CpuManager exists
            if SystemOperation.mm is None:
                SystemOperation.mm = MemoryManager(1024, 2)  # Example sizes
            return Process(arg)
        elif type == "DELETE_PROCESS":
            SystemOperation.mm.delete(arg)
        return None
