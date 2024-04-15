class FrameMemory:
    def __init__(self, pageNum, displacement):
        self.pageNum = pageNum
        self.displacement = displacement

    def get_page_num(self):
        return self.pageNum

    def set_page_num(self, pageNum):
        self.pageNum = pageNum

    def get_displacement(self):
        return self.displacement

    def set_displacement(self, displacement):
        self.displacement = displacement