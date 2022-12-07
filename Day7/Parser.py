from FileSystem import FileSystem


class Parser:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')
        self.current_directory = ""
        self.filesystem = FileSystem()

    def construct_filesystem(self):
        line = self.file.readline().strip()
        while True:
            if line == '':
                break

            if self.__is_cd(line):
                folder = self.__get_cd_arg(line)
                self.filesystem.change_directory(folder)
                line = self.file.readline().strip()
            elif self.__is_ls(line):
                line = self.__apply_ls_output()
        self.filesystem.reset()
        return self.filesystem

    @staticmethod
    def __is_cd(line):
        return line[0:4] == "$ cd"

    @staticmethod
    def __get_cd_arg(line):
        return line.replace("$ cd ", "")

    def __apply_ls_output(self):
        while True:
            line = self.file.readline().strip()
            if self.__is_command(line) or line == '':
                return line

            parsed_output = self.__parse_ls_output(line)

            if parsed_output[0] == "dir":
                self.filesystem.create_directory(parsed_output[1])
            else:
                self.filesystem.create_file(parsed_output[2], parsed_output[1])

    @staticmethod
    def __parse_ls_output(line):
        if line[0:3] == "dir":
            return line.split(" ")
        else:
            file_details = line.split(" ")
            file_details[0] = int(file_details[0])
            file_details.insert(0, "file")
            return file_details

    def __is_command(self, line):
        return self.__is_ls(line) or self.__is_cd(line)

    @staticmethod
    def __is_ls(line):
        return line[0:4] == "$ ls"
