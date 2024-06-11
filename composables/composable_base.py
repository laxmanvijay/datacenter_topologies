"""
Composables are plug and play utilities that can be added to any topology object at any point.
They are defined to help with defining networkx constructs for plotting the defined graphs, mininet for network topology generation, etc.
"""
class Composable:
    def add_node(self, n: str):
        pass

    def add_edge(self, n1: str, n2: str):
        pass

    def remove_edge(self, n1: str, n2: str):
        pass




    


        

    