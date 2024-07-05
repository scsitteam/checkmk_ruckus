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

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    migrate_to_password,
    Password,
    SingleChoice,
    SingleChoiceElement,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _form_special_agent_ruckus_smartzone() -> Dictionary:
    return Dictionary(
        title=Title("Ruckus Smartzone Server"),
        elements = {
            "url": DictElement(
                parameter_form=String(
                    title=Title("Base-URL of the Smartzone Public API"),
                    custom_validate=(
                        validators.Url(
                            [validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS],
                        ),
                    ),
                    prefill=InputHint('https://HOST:8443/wsg/api/public'),
                ),
                required=True,
            ),
            "username": DictElement(
                parameter_form=String(
                    title=Title("Username"),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    migrate=migrate_to_password
                ),
                required=True,
            ),
            "ignore_cert": DictElement(
                parameter_form=SingleChoice(
                    elements=[
                        SingleChoiceElement(name='check_cert', title=Title('Check SSL Certificate')),
                        SingleChoiceElement(name='ignore_cert', title=Title('Ignore SSL Certificate')),
                    ],
                    prefill=DefaultValue('check_cert'),
                ),
                required=True,
            ),
        },
    )


rule_spec_ruckus_smartzone_datasource = SpecialAgent(
    name='ruckus_smartzone',
    title=Title('Ruckus Smartzone'),
    topic=Topic.APPLICATIONS,
    parameter_form=_form_special_agent_ruckus_smartzone,
)
