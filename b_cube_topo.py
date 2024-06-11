from base_topo import Graph

# The following implementation is based on the bcube paper: http://ccr.sigcomm.org/online/files/p63.pdf
class BCubeTopo(Graph):
    def __init__(self, n, k) -> None:
        super().__init__("b-cube")

        self.k = k # level in bcube starts from 0 ( total number of levels )
        self.n = n # denoted as n in the paper ( number of servers in each cube )

        self.num_hosts = n ** (k + 1)

        self.hosts = [('h_' + str(i), {'type': 'host'})
             for i in range (1, self.num_hosts + 1)]
        
        self.switches = []

    """
    BCell is a recursive topology. The implementation is as follows:
    * Generate hosts for the bottom layer
    * For each layer above, connect each of the switch to the host such that the connections are n ** k distance apart.
    """
    def generate_bcube_structure(self) -> None:
        self.create_nodes_from_array(self.hosts)

        for curr_level in range(0, self.k + 1):
            for j in range(0, self.n ** self.k):
                switch = self.add_node(f's_{curr_level}_{j}', 'switch')

                self.switches.append(switch)

                hosts_to_connect = range(j, j + self.n ** (curr_level + 1), self.n ** curr_level)

                for h in hosts_to_connect:
                    self.add_edge(switch.id, self.hosts[h][0])