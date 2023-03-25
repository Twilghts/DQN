from ospf_network import Ospf

if __name__ == '__main__':
    ospf_network = Ospf()
    for i in range(10):
        ospf_network.update_dataset()
        print(ospf_network.get_net_state())
        print("*************************************\n")
    for i in range(250):
        ospf_network.update_dataset(is_create_data=False)
        print(ospf_network.get_net_state())
        print("*************************************\n")
