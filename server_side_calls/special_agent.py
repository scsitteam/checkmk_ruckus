#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2024  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from collections.abc import Iterator

from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentCommand, SpecialAgentConfig


class Params(BaseModel):
    url: str
    username: str
    password: Secret
    ignore_cert: str | None


def commands_function(
    params: Params,
    host_config: HostConfig,
) -> Iterator[SpecialAgentCommand]:
    command_arguments: list[str | Secret] = [
        '--url', params.url,
        '--username', params.username,
        '--password', params.password.unsafe(),
    ]
    if params.ignore_cert == 'ignore_cert':
        command_arguments += ['--ignore-cert']
    yield SpecialAgentCommand(command_arguments=command_arguments)


special_agent_jb_fls = SpecialAgentConfig(
    name='ruckus_smartzone',
    parameter_parser=Params.model_validate,
    commands_function=commands_function,
)
