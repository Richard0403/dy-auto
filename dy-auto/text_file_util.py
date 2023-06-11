import codecs

class TextFile:

    def write_file(self, filePath: str, u, encoding="gbk"):
        with codecs.open(filePath, "w", encoding) as f:
            f.write(u)

    def read_file(self, filePath, encoding="utf-8"):
        with codecs.open(filePath, "r", encoding) as f:
            return f.read()

    def UTF8_2_GBK(self, src, dst):
        content = self.read_file(src, encoding="utf-8")
        self.write_file(dst, content, encoding="gbk")

    def Unicode_2_UTF8(self, src, dst):
        content = self.read_file(src, encoding="utf-8")
        self.write_file(dst, content, encoding="utf-8")



