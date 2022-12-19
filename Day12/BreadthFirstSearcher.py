class BreadthFirstSearcher:
    def __init__(self, graph):
        self.graph = graph
        self.paths = [{"current_square": graph.start, "length": 0}]
        graph.start.mark_visited()

    def search(self):
        while True:
            new_paths = []
            for path in self.paths:
                directions = path["current_square"].connected_squares
                for direction in directions:
                    if direction.end:
                        return path["length"] + 1
                    if direction.visited:
                        continue
                    else:
                        direction.mark_visited()
                        new_path = {"current_square": direction, "length": path["length"] + 1}
                        new_paths.append(new_path)
            if len(new_paths) == 0:
                return None
            self.paths = new_paths