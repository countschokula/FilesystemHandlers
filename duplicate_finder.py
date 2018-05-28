import argparse
from pathlib import Path
import hashlib
import json
"find duplicates in file system"


def test_equals():
    pass


class UniqueFileContainer:
    unique_files = {}
    path_save = "path"
    oc_save = "occurrences"
    file_save = "file"
    type_save = "type"

    def add(self, file, path):
        # TODO at tbe moment there are no directories here
        f_type = "dir" if path.is_dir else path.suffix()
        # TODO decide how files (and dir should be hashed)
        hashed_file = self.hash(file)
        if self.unique_files:
            self.unique_files[hashed_file] = {self.path_save: [str(path)], self.type_save: f_type, self.oc_save: 1}
        else:
            if self.unique_files.get(hashed_file):
                self.unique_files[hashed_file][self.path_save] = self.unique_files.get(hashed_file).get(self.path_save)\
                    .append(str(path))
                self.unique_files[hashed_file][self.oc_save] = self.unique_files.get(hashed_file).get(self.oc_save) + 1
            else:
                self.unique_files[hashed_file] = {self.path_save: [str(path)], self.type_save: f_type, self.oc_save: 1}

    def get_path_list(self, file):
        """if file is in uniques return list of path the file can be found, else return None"""
        h = self.hash(file)
        if self.unique_files.get(h):
            return self.unique_files[h].get(self.path_save)
        else:
            return None

    def get_file_hash(self, path):
        """"if path is in uniques return hash of file, else return false, function cheats as it checks filesystem
        and not self"""

        pass

    def save(self, output):
        with open(output, "w") as outfile:
            json.dump(self.unique_files, outfile)

    @staticmethod
    def hash(file):
        m = hashlib.md5()
        m.update(file)
        return m.hexdigest()


if __name__ == '__main__':

    # read commandline arguments, first
    help_text = "this is the help test"
    parser = argparse.ArgumentParser(help_text)
    # add arguments
    parser.add_argument("-D", "--directory", help="directory to start")
    parser.add_argument("-o", "--output", help="saves a json to output file")
    parser.add_argument("-r", "--recursive", help="include all sub-folders", action='store_true')
    parser.add_argument("-t", "--test", help="runs a test to see if hash and file is equal", action="store_true")

    args = parser.parse_args()
    container = UniqueFileContainer()
    path_stack = [Path(args.directory)]

    if args.test:
        test_equals()

    while path_stack:
        path = path_stack.pop()
        for child in path.iterdir():
            if child.is_dir():
                # TODO handle duplicate folders structures with heuristic? hash of subtree
                if args.recursive:
                        path_stack.append(child)
            if child.is_file():
                with open(child, 'rb') as f:
                    file = f.read()
                container.add(file, child)
    if args.output:
        container.save(args.output)

# TODO add some statistics ;;; is there any way to automaticaly resolve duplication?