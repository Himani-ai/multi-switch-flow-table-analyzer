from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub


class MultiSwitchFlowTableAnalyzer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MultiSwitchFlowTableAnalyzer, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self.monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.datapaths[datapath.id] = datapath
            self.logger.info("Switch %s connected", datapath.id)
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]
                self.logger.info("Switch %s disconnected", datapath.id)

    def monitor(self):
        while True:
            for dp in self.datapaths.values():
                self.request_flow_stats(dp)
            hub.sleep(5)

    def request_flow_stats(self, datapath):
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        datapath_id = ev.msg.datapath.id
        body = ev.msg.body

        print("\n===== Switch {} Flow Table =====".format(datapath_id))

        for stat in body:
            if stat.packet_count > 0:
                status = "ACTIVE"
            else:
                status = "UNUSED"

            print("Match   :", stat.match)
            print("Priority:", stat.priority)
            print("Packets :", stat.packet_count)
            print("Bytes   :", stat.byte_count)
            print("Duration:", stat.duration_sec, "sec")
            print("Status  :", status)
            print("-----------------------------")

