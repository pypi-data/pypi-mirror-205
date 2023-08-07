# GENERATED CODE - DO NOT MODIFY
from __future__ import annotations
import chitose

def notify_of_update(service: str, headers: dict[str, str], hostname: str):
    """Notify a crawling service of a recent update. Often when a long break between updates causes the connection with the crawling service to break."""
    return chitose.xrpc.call('com.atproto.sync.notifyOfUpdate', [('hostname', hostname)], None, service, {} | headers)