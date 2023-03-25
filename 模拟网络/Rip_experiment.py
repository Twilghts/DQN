from rip_network import Rip

if __name__ == '__main__':
    rip_network = Rip()
    for i in range(10):
        rip_network.update_dataset()
        print(rip_network.get_net_state())
        print("*************************************\n")
    for i in range(250):
        rip_network.update_dataset(is_create_data=False)
        print(rip_network.get_net_state())
        print("*************************************\n")
