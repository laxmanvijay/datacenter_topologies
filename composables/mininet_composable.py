from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

from .composable_base import Composable

class MininetComposer(Topo, Composable):
    def __init__(self) -> None:
        super().__init__()

        Topo.__init__()

        self.host_list = {}

    def add_node(self, name: str, type: str) -> None:
        h = None
        if type == "host":
            h = self.addHost( name )
        else:
            h = self.addSwitch( name )
        
        self.host_list[name] = h
    
    def add_edge(self, n1: str, n2: str) -> None:
        self.addLink( self.host_list[n1], self.host_list[n2] )

    def remove_edge(self, n1: str, n2: str) -> bool:
        return False

    def run():
        topo = MininetComposer()
        net = Mininet(topo=topo,
                    switch=OVSKernelSwitch,
                    link=TCLink,
                    controller=None)
        net.addController(
            'c1', 
            controller=RemoteController, 
            ip="127.0.0.1", 
            port=6653)
        net.start()
        CLI(net)
        net.stop()