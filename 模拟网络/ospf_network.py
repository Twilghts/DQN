from net import Net


class Ospf(Net):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    ospf_net = Ospf()
    # for router in ospf_net.routers:
    #     print(f'路由器序号:{router.sign},对应的路由表:{router.routing_table}')
    print(ospf_net.routers)
    print(ospf_net.links)
