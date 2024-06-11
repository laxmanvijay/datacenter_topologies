from base_topo import Graph
from typing import List
from composables.networkx_composable import NetworkxVisualizationComposer

# The following implementation is based on the fat tree datacenter architecture paper: http://ccr.sigcomm.org/online/files/p63-alfares.pdf
class FatTreeTopo(Graph):
    def __init__(self, pod_count) -> None:
        super().__init__("fat-tree")

        self.num_pods = pod_count
        self.num_hosts = int((pod_count ** 3) / 4) # fat tree supports (k^3)/4 hosts

        self.num_agg_switches  = pod_count ** 2 # including both the layers of the aggregate switch k^2
        self.num_core_switches = int(self.num_agg_switches / 4) # (k/2)^2 core switches

        # random generation of hosts and switches
        self.hosts = [('h_' + str(i), {'type': 'host'})
             for i in range (1, self.num_hosts + 1)]

        self.core_switches = [('s_c_' + str(i), {'type':'switch'})
                        for i in range(1, self.num_core_switches + 1)]

        self.agg_switches = [('s_a_' + str(i), {'type':'switch'})
                        for i in range(1, self.num_agg_switches + 1)]

    """
    The below function generates a fat tree topology with the following configuration:
    * There are hosts connected to edge switches
    * Each edge switch is connected to aggregate switches of its own pod
    * Each aggregate switch then connects to core switches

    * The aggregate switches are divided into two layers - top layer and bottom layer
    """
    def generate_fat_tree_structure(self):
        self.create_nodes_from_array(self.hosts)
        self.create_nodes_from_array(self.core_switches)
        self.create_nodes_from_array(self.agg_switches)

        host_offset = 0
        for pod in range(self.num_pods):
            core_idx = 0
            for i in range(self.num_pods // 2): # iterating and obtaining the aggregate switch one by one for each pod
                switch = self.agg_switches[(self.num_pods * pod) + i][0]

                # Every pod has k/2 aggregate switches that are connected to the core switches
                # For every pod, we connect the aggregate switch to the core such that there is a 
                # connection to each of the core switch.
                # 
                # In a k-port aggregate switch, k/2 ports are connected to the core and the remaining
                # is connected to the edge switches.
                for port in range(0, self.num_pods // 2):

                    core_switch = self.core_switches[core_idx][0]

                    self.add_edge(switch, core_switch)
                    self.add_edge(core_switch, switch)

                    core_idx += 1

                # Connect to the edge switches
                for port in range(self.num_pods // 2, self.num_pods):

                    edge_switch = self.agg_switches[(self.num_pods * pod) + port][0]

                    self.add_edge(switch, edge_switch)
                    self.add_edge(edge_switch, switch)

            # Connect each of the edge switch to the hosts
            for i in range(self.num_pods // 2, self.num_pods):
                switch = self.agg_switches[(self.num_pods * pod) + i][0]

                # Connect to hosts
                for _ in range(self.num_pods // 2, self.num_pods): # First k/2 agg switches connect to upper layer
                    host = self.hosts[host_offset][0]


                    self.add_edge(switch, host)
                    self.add_edge(host, switch)

                    host_offset += 1

if __name__ == "__main__":
    ftt = FatTreeTopo(14)
    n = NetworkxVisualizationComposer()
    ftt.add_composable(n)
    ftt.generate_fat_tree_structure()
    # hosts = ftt.get_all_hosts()
    # res = []
    # for i in range(0, len(hosts)):
    #     t_res = []
    #     remaining_hosts = hosts[0:i] + hosts[i+1:len(hosts)]
    #     print(f"host {i+1} of {len(hosts)}")
    #     for rem in remaining_hosts:
    #         path_name = None
    #         # if computed_paths.get(f"{hosts[idx].id}:{rem.id}") != None:
    #         #     path_name = f"{hosts[idx].id}:{rem.id}"
    #         # elif computed_paths.get(f"{rem.id}:{hosts[idx].id}") != None:
    #         #     path_name = f"{rem.id}:{hosts[idx].id}"
            
    #         # if path_name != None:
    #         #     t_res.append(computed_paths[path_name])
            
    #         # else:
    #             # path_name = f"{hosts[idx].id}:{rem.id}"
    #             # computed_paths[path_name] = self.compute_dijikstra(hosts[idx], rem)
    #         t_res.append(n.compute_dijkstra(hosts[i].id, rem.id))
    #     res.extend(t_res)
    all_dj = ftt.compute_dijikstra_for_all_hosts()