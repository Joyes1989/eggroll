# -*- coding: utf-8 -*-
#  Copyright (c) 2019 - now, Eggroll Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from eggroll.core.conf_keys import SessionConfKeys, TransferConfKeys, \
    ClusterManagerConfKeys, NodeManagerConfKeys
from eggroll.core.constants import DeployModes
from eggroll.core.constants import ProcessorTypes, ProcessorStatus
from eggroll.core.constants import StoreTypes
from eggroll.core.meta_model import ErStore, ErStoreLocator, ErEndpoint, \
    ErProcessor
from eggroll.core.session import ErSession
from eggroll.roll_pair.roll_pair import RollPairContext

ER_STORE1 = ErStore(
    store_locator=ErStoreLocator(store_type=StoreTypes.ROLLPAIR_LEVELDB,
                                 namespace="namespace",
                                 name="name"))


def get_debug_test_context(is_standalone=False):
    manager_port = 4671
    egg_ports = [20001]
    egg_transfer_ports = [20002]
    self_server_node_id = 2

    options = {}
    if is_standalone:
        options[SessionConfKeys.CONFKEY_SESSION_DEPLOY_MODE] = "standalone"
    options[TransferConfKeys.CONFKEY_TRANSFER_SERVICE_HOST] = "localhost"
    options[TransferConfKeys.CONFKEY_TRANSFER_SERVICE_PORT] = "20002"
    options[ClusterManagerConfKeys.CONFKEY_CLUSTER_MANAGER_PORT] = str(manager_port)
    options[NodeManagerConfKeys.CONFKEY_NODE_MANAGER_PORT] = str(manager_port)

    egg = ErProcessor(id=1,
                      server_node_id=self_server_node_id,
                      processor_type=ProcessorTypes.EGG_PAIR,
                      status=ProcessorStatus.RUNNING,
                      command_endpoint=ErEndpoint("localhost", egg_ports[0]),
                      transfer_endpoint=ErEndpoint("localhost",
                                                   egg_transfer_ports[0]))

    roll = ErProcessor(id=1,
                       server_node_id=self_server_node_id,
                       processor_type=ProcessorTypes.ROLL_PAIR_MASTER,
                       status=ProcessorStatus.RUNNING,
                       command_endpoint=ErEndpoint("localhost", manager_port))

    session = ErSession(session_id='testing',
                        processors=[egg, roll],
                        options=options)
    # session = ErSession(options={})
    context = RollPairContext(session)
    return context


def get_standalone_context():
    options = {}
    options[SessionConfKeys.CONFKEY_SESSION_DEPLOY_MODE] = DeployModes.STANDALONE

    session = ErSession(options=options)
    print(session.get_session_id())
    context = RollPairContext(session)

    return context

def get_cluster_context():
    options = {}
    options[ClusterManagerConfKeys.CONFKEY_CLUSTER_MANAGER_HOST] = "localhost"
    options[ClusterManagerConfKeys.CONFKEY_CLUSTER_MANAGER_PORT] = "4671"

    session = ErSession(options=options)
    print(session.get_session_id())
    context = RollPairContext(session)

    return context