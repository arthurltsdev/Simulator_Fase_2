class FrameMemory:
    def __init__(self, page_num, offset):
        self.page_num = page_num
        self.offset = offset

    def get_page_num(self):
        return self.page_num

    def set_page_num(self, page_num):
        self.page_num = page_num

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
