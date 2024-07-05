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

from cmk.graphing.v1 import graphs, metrics, perfometers, translations, Title

translation_smartzone_ap = translations.Translation(
    name='smartzone_ap',
    check_commands=[translations.PassiveCheck('smartzone_ap')],
    translations={
        'latency_24': translations.ScaleBy(0.000001),
        'latency_5': translations.ScaleBy(0.000001),
        'latency_6': translations.ScaleBy(0.000001),
    }
)

metric_clients_24 = metrics.Metric(
    name='clients_24',
    title=Title('Clients 2.4G'),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.DARK_BLUE,
)
metric_clients_5 = metrics.Metric(
    name='clients_5',
    title=Title('Clients 5G'),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.BLUE,
)
metric_clients_6 = metrics.Metric(
    name='clients_6',
    title=Title('Clients 6G'),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.LIGHT_BLUE,
)

metric_airtime_24 = metrics.Metric(
    name='airtime_24',
    title=Title('Airtime 2.4G'),
    unit=metrics.Unit(metrics.DecimalNotation("%"), metrics.StrictPrecision(0)),
    color=metrics.Color.DARK_PURPLE,
)
metric_airtime_5 = metrics.Metric(
    name='airtime_5',
    title=Title('Airtime 5G'),
    unit=metrics.Unit(metrics.DecimalNotation("%"), metrics.StrictPrecision(0)),
    color=metrics.Color.PURPLE,
)
metric_airtime_6 = metrics.Metric(
    name='airtime_6',
    title=Title('Airtime 6G'),
    unit=metrics.Unit(metrics.DecimalNotation("%"), metrics.StrictPrecision(0)),
    color=metrics.Color.LIGHT_PURPLE,
)

metric_latency_24 = metrics.Metric(
    name='latency_24',
    title=Title('Latency 2.4G'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.DARK_ORANGE,
)
metric_latency_5 = metrics.Metric(
    name='latency_5',
    title=Title('Latency 5G'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.ORANGE,
)
metric_latency_6 = metrics.Metric(
    name='latency_6',
    title=Title('Latency 6G'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.LIGHT_ORANGE,
)

metric_noise_24 = metrics.Metric(
    name='noise_24',
    title=Title('Noise 2.4G'),
    unit=metrics.Unit(metrics.DecimalNotation("dBm")),
    color=metrics.Color.DARK_BROWN,
)
metric_noise_5 = metrics.Metric(
    name='noise_5',
    title=Title('Noise 5G'),
    unit=metrics.Unit(metrics.DecimalNotation("dBm")),
    color=metrics.Color.BROWN,
)
metric_noise_6 = metrics.Metric(
    name='noise_6',
    title=Title('Noise 6G'),
    unit=metrics.Unit(metrics.DecimalNotation("dBm")),
    color=metrics.Color.LIGHT_BROWN,
)

graph_clients = graphs.Graph(
    name='clients',
    title=Title('Clients'),
    compound_lines=['clients_24', 'clients_5', 'clients_6'],
)

graph_airtime = graphs.Graph(
    name='airtime',
    title=Title('Airtime'),
    minimal_range=graphs.MinimalRange(0, 100),
    simple_lines=['airtime_24', 'airtime_5', 'airtime_6'],
    optional=['airtime_24', 'airtime_5', 'airtime_6'],
)

graph_latency = graphs.Graph(
    name='latency',
    title=Title('Latency'),
    simple_lines=['latency_24', 'latency_5', 'latency_6'],
    optional=['latency_24', 'latency_5', 'latency_6'],
)

graph_noise = graphs.Graph(
    name='noise',
    title=Title('Noise Floor'),
    minimal_range=graphs.MinimalRange(-100, -75),
    simple_lines=['noise_24', 'noise_5', 'noise_6'],
    optional=['noise_24', 'noise_5', 'noise_6'],
)

perfometer_clients = perfometers.Perfometer(
    name = 'clients',
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(1)),
    segments=['clients_24', 'clients_5', 'clients_6'],
)


UNIT_BYTES_PER_SECOND = metrics.Unit(metrics.IECNotation("B/s"))
UNIT_BITS_PER_SECOND = metrics.Unit(metrics.IECNotation("bits/s"))
UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(""))

metric_if24_in_octets = metrics.Metric(
    name="if24g_in_octets",
    title=Title("2.4G Input octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.DARK_GREEN,
)
metric_if5_in_octets = metrics.Metric(
    name="if5g_in_octets",
    title=Title("5G Input octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.GREEN,
)
metric_if6_in_octets = metrics.Metric(
    name="if6g_in_octets",
    title=Title("6G Input octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.LIGHT_GREEN,
)

metric_i24_out_octets = metrics.Metric(
    name="if24g_out_octets",
    title=Title("2.4G Output octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.DARK_BLUE,
)
metric_if5_out_octets = metrics.Metric(
    name="if5g_out_octets",
    title=Title("5G Output octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.BLUE,
)
metric_if6_out_octets = metrics.Metric(
    name="if6g_out_octets",
    title=Title("6G Output octets"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.LIGHT_BLUE,
)

graph_bandwidth_smartzone_ap_translated = graphs.Bidirectional(
    name="bandwidth_smartzone_ap_translated",
    title=Title("Bandwidth"),
    lower=graphs.Graph(
        name="bandwidth_translated_out",
        title=Title("Bandwidth"),
        compound_lines=[
            metrics.Product(
                Title("2.4G Output bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.DARK_BLUE,
                ['if24g_out_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.DARK_BLUE, 8.0)],
            ),
            metrics.Product(
                Title("5G Output bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.BLUE,
                ['if5g_out_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.BLUE, 8.0)],
            ),
            metrics.Product(
                Title("6G Output bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.LIGHT_BLUE,
                ['if6g_out_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.LIGHT_BLUE, 8.0)],
            ),
        ],
    ),
    upper=graphs.Graph(
        name="bandwidth_translated_in",
        title=Title("Bandwidth"),
        compound_lines=[
            metrics.Product(
                Title("2.4G Input bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.DARK_GREEN,
                ['if24g_in_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.DARK_GREEN, 8.0)],
            ),
            metrics.Product(
                Title("5G Input bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.GREEN,
                ['if5g_in_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.GREEN, 8.0)],
            ),
            metrics.Product(
                Title("6G Input bandwidth"),
                UNIT_BITS_PER_SECOND,
                metrics.Color.LIGHT_GREEN,
                ['if6g_in_octets', metrics.Constant(Title(""), UNIT_NUMBER, metrics.Color.LIGHT_GREEN, 8.0)],
            ),
        ],
    ),
)

perfometer_if_smartzone_ap_octets = perfometers.Bidirectional(
    name='if_smartzone_ap_octets',
    left=perfometers.Perfometer(
        name='if_smartzone_ap_in_octets',
        focus_range=perfometers.FocusRange(
            perfometers.Closed(0),
            perfometers.Open(500000),
        ),
        segments=['if24g_in_octets', 'if5g_in_octets', 'if6g_in_octets'],
    ),
    right=perfometers.Perfometer(
        name='if_smartzone_ap_out_octets',
        focus_range=perfometers.FocusRange(
            perfometers.Closed(0),
            perfometers.Open(500000),
        ),
        segments=['if24g_out_octets', 'if5g_out_octets', 'if6g_out_octets'],
    ),
)
