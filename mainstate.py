
class MainState:
    def __init__(self):
        self.nodes_clicked = []
        self.editing_province = False
        self.creating_neighbours = False
        self.first_nei = None
        self.running = True

    def reset_state(self):
        self.nodes_clicked = []
        self.editing_province = False
        self.creating_neighbours = False
        self.first_nei = None
