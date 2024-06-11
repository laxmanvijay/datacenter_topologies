from base_topo import Graph
import numpy as np

# The following implementation is based on the jellyfish topology paper: https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf
class JellyFishTopo(Graph):
    def __init__(self, pod_count: int) -> None:
        super().__init__("jelly-fish")

        self.num_pods = pod_count
        self.open = []

        self.num_hosts  = int((pod_count ** 3) / 4) # including both the layers of the aggregate switch k^2

        self.num_switches  = int((pod_count ** 2) * 5/4) # calculating number of switches using the sum of aggregate and core switches from fat-tree

        # random generation of hosts and switches
        self.hosts = [('h_' + str(i), {'type': 'host'})
             for i in range (1, self.num_hosts + 1)]

        self.switches = [('s_' + str(i), {'type':'switch', 'available_ports': pod_count})
                        for i in range(1, self.num_switches + 1)]

    """
    The below function generates jellyfish topology based on the following structure

    * Each of the hosts are connected to a random switch
    * Each of the switches are then interconnected randomly. For this implementation, a uniform random distribution is used.
    * Each of the switches are connected until the number of available ports for each switch is exhausted.
    """
    def generate_jellyfish_structure(self):
        self.create_nodes_from_array(self.hosts)
        self.create_nodes_from_array(self.switches)

        # connect host and port randomly using uniform distribution
        for h in self.hosts:
            chosen_switch_idx = np.random.randint(0, len(self.switches))

            self.add_edge(h[0], self.switches[chosen_switch_idx][0])
        
        for s in self.switches:
            while s[1].get('available_ports') >= 0: # 1 is the previously added host
                chosen_switch_idx = np.random.randint(0, len(self.switches))

                chosen = self.switches[chosen_switch_idx]

                if chosen[1]['available_ports'] == 0:
                    continue

                if chosen[0] == s[0]:
                    continue

                self.add_edge(s[0], chosen[0])
                
                chosen[1]['available_ports'] -= 1
                s[1]['available_ports'] -= 1


        

