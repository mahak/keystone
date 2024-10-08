# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

from keystone.conf import utils

driver = cfg.StrOpt(
    'driver',
    default='sql',
    help=utils.fmt(
        """
Entry point for the domain-specific configuration driver in the
`keystone.resource.domain_config` namespace. Only a `sql` option is provided by
keystone, so there is no reason to set this unless you are providing a custom
entry point.
"""
    ),
)

caching = cfg.BoolOpt(
    'caching',
    default=True,
    help=utils.fmt(
        """
Toggle for caching of the domain-specific configuration backend. This has no
effect unless global caching is enabled. There is normally no reason to disable
this.
"""
    ),
)

cache_time = cfg.IntOpt(
    'cache_time',
    default=300,
    help=utils.fmt(
        """
Time-to-live (TTL, in seconds) to cache domain-specific configuration data.
This has no effect unless `[domain_config] caching` is enabled.
"""
    ),
)

additional_whitelisted_options = cfg.Opt(
    'additional_whitelisted_options',
    type=cfg.types.Dict(value_type=cfg.types.List(bounds=True)),
    help=utils.fmt(
        """
Additional whitelisted domain-specific options for out-of-tree drivers.
This is a dictonary of lists with the key being the group name and value a list
of group options."""
    ),
)

additional_sensitive_options = cfg.Opt(
    'additional_sensitive_options',
    type=cfg.types.Dict(value_type=cfg.types.List(bounds=True)),
    help=utils.fmt(
        """
Additional sensitive domain-specific options for out-of-tree drivers.
This is a dictonary of lists with the key being the group name and value a list
of group options."""
    ),
)


GROUP_NAME = __name__.split('.')[-1]
ALL_OPTS = [
    driver,
    caching,
    cache_time,
    additional_whitelisted_options,
    additional_sensitive_options,
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}
