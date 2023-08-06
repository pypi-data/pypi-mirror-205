"""
"""
from scinode.engine import EngineNodeTree
from scinode.engine import EngineNode
from scinode.database.client import scinodedb
from scinode.engine.config import broker_queue_name
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.mq import Consumer
import traceback
import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class EngineScheduler(Consumer):
    """Engine Scheduler Class.

    Example:

    >>> en = EngineScheduler(queue=mq)
    >>> en.consume_messages()
    """

    coll_name = "scheduler"

    def process(self, msg):
        """process message"""
        print(f"process: {msg}")
        try:
            uuid, catalog, body = msg.split(",")
        except Exception as e:
            print(e)
            return 1
        if catalog == "nodetree":
            try:
                self.apply_nodetree_message(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {"error": str(error)}}
                )
                return 1
        elif catalog == "node":
            try:
                self.apply_node_message(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                data = msg.split(":")
                name = data[0]
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "FAILED"}}
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.error": str(error)}}
                )
                return 1
        elif catalog == "scheduler":
            try:
                self.apply_consumer_action(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(
                        str(error)
                    )
                )
                return 1
        else:
            raise Exception(f"Unknown type {catalog}")
            return 1

        return 0

    def apply_nodetree_message(self, uuid, msg):
        # print("apply_nodetree_message: ", msg)
        key, value = msg.split(":")
        # print(name, m)
        nodetree = EngineNodeTree(uuid=uuid)
        if key == "action":
            nodetree.apply_nodetree_action(value)
        elif key == "state":
            nodetree.apply_nodetree_state(value)

    def apply_node_message(self, uuid, msg):
        """apply action to all nodes"""
        from scinode.database.client import scinodedb
        from scinode.utils.db import write_log
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        # print(f"apply_node_message: {msg}")
        data = msg.split(":")
        if len(data) == 3:
            name, key, value = data
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.{key}": value}}
            )
            # push message to child node
            ntdata = scinodedb["nodetree"].find_one(
                {"uuid": uuid}, {f"nodes.{name}.uuid": 1}
            )
            node_uuid = ntdata["nodes"][name]["uuid"]
            # print(f"node uuid: {node_uuid}, {key}: {value}")
            child_nodes = scinodedb["node"].find(
                {"metadata.ref_uuid": node_uuid}, {"metadata": 1, "name": 1}
            )
            if child_nodes is not None:
                for child in child_nodes:
                    msg = f"{child['metadata']['nodetree_uuid']},node,{name}:{key}:{value}"
                    send_message_to_queue(broker_queue_name, msg)
            # push message to parent nodetree
            if key == "state" and value not in ["RUNNING"]:
                self.update_nodetree_state(uuid)
                record = scinodedb["node"].find_one(
                    {"name": name, "metadata.nodetree_uuid": uuid}, {"metadata": 1}
                )
                if record["metadata"]["scattered_from"]:
                    parent_node = scinodedb["node"].find_one(
                        {"uuid": record["metadata"]["scattered_from"]}, {"metadata": 1}
                    )
                    msg = f"{parent_node['metadata']['nodetree_uuid']},node,scatter:{record['metadata']['scattered_label']}:{msg}"
                    print("push parent: ", msg)
                    send_message_to_queue(broker_queue_name, msg)
            if key == "action":
                self.apply_node_action(uuid, name, value)
        elif len(data) == 5:
            # scatter node, e.g scatter:0:add2:state:FINISHED
            key1, label, name, key2, value = data
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.{key1}.{label}": value}}
            )
            self.update_nodetree_state(uuid)
        write_log({"metadata.nodetree_uuid": uuid, "name": name}, f"\n{msg}\n", "node")
        # logger.debug("apply_node_message, time: {}".format(time.time() - tstart))

    def apply_node_action(self, uuid, name, action):
        tstart = time.time()
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"apply_node_action: {name}, {action}")
        if action == "NONE":
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.action": "NONE"}}
            )
        elif action == "LAUNCH":
            self.launch_node(uuid, name)
        elif action == "EXPOSE_OUTPUTS":
            self.expose_outputs(uuid, name)
        elif action == "PAUSE":
            self.pause_node(uuid, name)
        elif action == "PLAY":
            self.play_node(uuid, name)
        elif action == "SKIP":
            self.skip_node(uuid, name)
        elif action == "RESET":
            self.reset_node(uuid, name)
        elif action == "RESET_LAUNCH":
            self.reset_node(uuid, name, launch=True)
        elif action == "FINISH":
            # TODO
            # self.record[name]["state"] = "FINISHED"
            pass
        # print("apply_node_action: ", self.record["nodes"])
        logger.debug("apply_node_action, time: {}".format(time.time() - tstart))

    def update_nodetree_state(self, uuid):
        """update nodetree state.

        If there is a node change its state, we need to call this funciton.
        """
        # print("\nUpdate nodetree: {}".format(uuid))
        nodetree = EngineNodeTree(uuid=uuid)
        nodetree.update_nodetree_state()
        del nodetree

    def pause_node(self, uuid, name):
        """Pause node.

        Args:
            name (str): name of the node to be paused
        """
        logger.debug("pause node, name: {}".format(name))
        ndata = scinodedb["nodetree"].find_one({"uuid": uuid}, {f"nodes.{name}": 1})
        if ndata["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{ndata['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "PAUSED"}}
        )

    def play_node(self, uuid, name):
        """Play node.

        Args:
            name (str): name of the node to be played
        """
        logger.debug("play node, name: {}".format(name))
        ndata = scinodedb["nodetree"].find_one({"uuid": uuid}, {f"nodes.{name}": 1})
        if ndata["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{ndata['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "CREATED"}}
        )

    def skip_node(self, uuid, name):
        """Skip node.

        Args:
            name (str): name of the node to be skiped
        """
        nodes_to_skip = []
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"connectivity.child_node": 1}
        )
        child_nodes = ntdata["connectivity"]["child_node"][name]
        nodes_to_skip.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_skip:
            items[f"nodes.{name}.state"] = "SKIPPED"
        scinodedb["nodetree"].update_one({"uuid": uuid}, {"$set": items})

    def reset_node(self, uuid, name, launch=False):
        """Reset node and all its child nodes.
        If this node belong to a node group, we need to reset the node group.

        Args:
            name (str): name of the node to be paused
        """
        nodes_to_reset = [name]
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"state": 1, "connectivity.child_node": 1, "metadata": 1}
        )
        child_nodes = ntdata["connectivity"]["child_node"][name]
        nodes_to_reset.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_reset:
            items[f"nodes.{name}.state"] = "CREATED"
        if launch:
            for name in nodes_to_reset:
                items[f"nodes.{name}.action"] = "LAUNCH"
        # If the nodetree is FINISHED, we change it state to CREATED.
        if ntdata["state"] in ["FINISHED"]:
            items["state"] = "CREATED"
        scinodedb["nodetree"].update_one({"uuid": uuid}, {"$set": items})
        # reset the parent_node
        if ntdata["metadata"]["parent_node"]:
            item = scinodedb["node"].find_one(
                {"uuid": ntdata["metadata"]["parent_node"]},
                {"_id": 0, "name": 1, "metadata": 1},
            )
            msg = (
                f"{item['metadata']['nodetree_uuid']},node,{item['name']}:action:RESET"
            )
            send_message_to_queue(broker_queue_name, msg)
        # node group node

    def cancel_node(self, uuid, name):
        """Cancel node"""
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        uuid = ntdata["nodes"][name]["uuid"]
        future = self.futures.get(uuid)
        if future is not None:
            log = "Node is running: {}.\n".format(future.running())
            was_calcelled = future.cancel()
            if was_calcelled:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
                )
                log += "Node is cancelled: {}".format(was_calcelled)
                # self.update_db_keys({"outputs": {}})
            else:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                log += "Can not cancel node.".format()
        else:
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            log = "Future is None. Node {} is not running. Can not cancel.".format(
                self.dbdata["name"]
            )

    def stop_consumer(self, name):
        from scinode.daemon.scheduler import DaemonScheduler

        print(f"Sotp scheduler {name}...")
        # because the we can not update the index after stopping the daemon,
        # we update the queue index before that
        self.queue.update_index(self.queue.index + 1)
        worker = DaemonScheduler(name)
        worker.stop()

    def restart_consumer(self, name):
        import os

        print(f"Restart scheduler {name}...")
        scinodedb[self.coll_name].update_one(
            {"name": name}, {"$set": {"msg": [], "indices": [0]}}
        )
        os.system("scinode scheduler hard-restart")
