class FrameMemory:
    def __init__(self, pageNum, offset):
        self.pageNum = pageNum
        self.offset = offset

    def get_page_num(self):
        return self.pageNum

    def set_page_num(self, pageNum):
        self.pageNum = pageNum

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
