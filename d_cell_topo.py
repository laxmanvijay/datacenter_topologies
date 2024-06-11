from base_topo import Graph

# The following implementation is based on the dcell topology paper: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=bd2e28376aca5a8ef1cf6068a3aeb1ca6d0e1abd
class DCellTopo(Graph):
    def __init__(self, n, l) -> None:
        super().__init__("d-cell")

        self.l = l # level in dcell starts from 0 ( total number of levels )
        self.n = n # denoted as n in the paper ( number of servers in each cell )

        self.hosts = []
        
        self.create_nodes_from_array(self.hosts)
        
        self.switches = []

        self.switch_count = 0
        self.host_count = 0

        self.virtual_edge_count = 0

    """
    DCell is a recursive topology. The implementation is as follows:
    * Only at level 0, the hosts exists - Consequently, level 0 is the termination condition (base case)
    * When level = 0,
        * Create n hosts and attach it to the corresponding switch
        * Append each of the host to a host_arr and return it ( used for backtracking hosts in upper levels (level > 0) )
    * When level > 0,
        * Recursively generate lower levels and append the output of each level to a host array
        * Each of the lower level can be considered a virtual host
        * Connect each of the virtual host using the following logic:
            * Store a boolean 'connected' variable for each host
            * Choose two non-connected hosts and connect them
            * Set the connected variable to true
            * Once the iteration is over, reset connected to false so that, upper layer can connect the hosts ( backtracking reinitialization )
        * Return the temp host array
    * Once this process is over, we get a completed n-level dcell topology
     
    """
    def generate_dcell_structure(self, level: int) -> None:
        if level == 0:
            switch = self.add_node(f's_{level}_{self.switch_count}', 'switch')
            self.switch_count += 1

            temp_host_arr = []

            self.switches.append(switch)

            for i in range (self.n):
                h = f'h_{self.host_count}'
                self.host_count += 1

                self.add_node(h, 'host')
                self.host_count += 1

                temp_host_arr.append({
                    'host': h,
                    'connected': False
                })

                self.hosts.append(h)

                self.add_edge(switch.id, h)
            
            return temp_host_arr

        else:
            hosts_arr = []

            num_server_in_prev_level = self.get_num_server(level - 1)
            num_of_cells_in_curr_level = num_server_in_prev_level + 1

            for c in range(num_of_cells_in_curr_level):
                hosts_arr.append({c: self.generate_dcell_structure(level-1)})

            for i in range(num_of_cells_in_curr_level - 1):
                for j in range(i+1, num_of_cells_in_curr_level):
                    self.connect_virtual_hosts(hosts_arr[i], hosts_arr[j])

            out = []
            for sublist in hosts_arr:
                for k, v in sublist.items():
                    out.extend(v)
            
            for i in out:
                i['connected'] = False

            return out


    def connect_virtual_hosts(self, v1: list[dict[str, any]], v2: list[dict[str, any]]):
        n1 = list(filter(lambda x: x['connected'] == False, list(v1.values())[0]))[0]
        n2 = list(filter(lambda x: x['connected'] == False, list(v2.values())[0]))[0]

        n1['connected'] = True
        n2['connected'] = True

        self.virtual_edge_count += 1

        self.add_edge(n1['host'], n2['host'])
                    

    def get_num_server(self, level: int):
        if level == 0:
            return self.n
        
        serv_in_prev = self.get_num_server(level - 1)

        return serv_in_prev * (serv_in_prev + 1)

        

            
        



