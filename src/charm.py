#!/usr/bin/env python3
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

"""Charmed operator for OpenSearch, an open source search and analytics engine."""

import logging

from charms.observability_libs.v0.kubernetes_service_patch import KubernetesServicePatch
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class OpensearchCharm(CharmBase):
    """Charmed operator for OpenSearch, an open source search and analytics engine."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.opensearch_pebble_ready, self._on_opensearch_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.inject_action, self._on_inject_action)
        self.framework.observe(self.on.inject_action, self._on_inject_action)
        self.framework.observe(self.on.cred_action, self._on_creds_action)

        self._service_patcher = KubernetesServicePatch(self, [(self.app.name, 4080, 4080)])

    def _on_opensearch_pebble_ready(self, event):
        """Define and start a workload using the Pebble API.

        TEMPLATE-TODO: change this example to suit your needs.
        You'll need to specify the right entrypoint and environment
        configuration for your specific workload. Tip: you can see the
        standard entrypoint of an existing container using docker inspect

        Learn more about Pebble layers at https://github.com/canonical/pebble
        """
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload

        # TODO: fetch or generate creds
        
        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "opensearch layer",
            "description": "pebble config layer for opensearch",
            "services": {
                "opensearch": {
                    "override": "replace",
                    "summary": "opensearch",
                    # TODO: build args out of the config.
                    "command": "./opensearch-entrypoint.sh"
                    "startup": "enabled",
                    "environment": {
                        # TODO: add admin_user, admin_password, and other info.
                    },
                }
            },
        }
        # Add intial Pebble config layer using the Pebble API
        container.add_layer("opensearch", pebble_layer, combine=True)
        # Autostart any services that were defined with startup: enabled
        container.autostart()
        # Learn more about statuses in the SDK docs:
        # https://juju.is/docs/sdk/constructs#heading--statuses
        self.unit.status = ActiveStatus()

    def _on_config_changed(self, _):
        # TODO: config for dashboard, data set, etc.
        pass

    def _on_inject_action(self, event):
        """Injest a given dataset.

        TODO: what params to pass?
        """
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"injest": "Not yet implemented."})

    def _on_creds_action(self, event):
        """Return the admin creds."""
        username = "not yet implemeneted"
        password = "not yet implemented"


        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"username": username, "password": password})


if __name__ == "__main__":
    main(CharmOpensearchCharm)
