# Copyright 2022 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyjoulescope_driver import Driver


def parser_config(p):
    """Joulescope info."""
    p.add_argument('--verbose', '-v',
                   action='store_true',
                   help='Display verbose information.')
    p.add_argument('--open', '-o',
                   choices=['defaults', 'restore'],
                   default='defaults',
                   help='The device open mode.  Defaults to "defaults".')
    p.add_argument('device_path',
                   nargs='*',
                   help='The target device for this command.')
    return on_cmd


def version_to_str(version):
    if isinstance(version, str):
        return version
    v_patch = version & 0xffff
    v_minor = (version >> 16) & 0xff
    v_major = (version >> 24) & 0xff
    return f'{v_major}.{v_minor}.{v_patch}'


class Info:

    def __init__(self, device_paths):
        self._device_paths = device_paths
        self._meta = {}
        self._values = {}

    def _on_pub(self, topic, value):
        self._values[topic] = value

    def _on_metadata(self, topic, value):
        if topic[-1] == '$':
            topic = topic[:-1]
        self._meta[topic] = value

    def run(self, args):
        with Driver() as d:
            d.log_level = args.jsdrv_log_level
            devices = d.device_paths()
            if not len(self._device_paths):
                self._device_paths = devices
            for device_path in self._device_paths:
                if device_path not in devices:
                    print(f'Device {device_path} not found in:')
                    s = "  \n".join(devices)
                    print(f'  {s}')
                    return 1
                d.open(device_path, mode=args.open)
                fn = self._on_metadata  # use same bound method for unsubscribe
                d.subscribe(device_path, 'metadata_rsp_retain', fn)
                d.unsubscribe(device_path, fn)
                fn = self._on_pub  # use same bound method for unsubscribe
                d.subscribe(device_path, 'pub_retain', fn)
                d.unsubscribe(device_path, fn)
                if args.verbose:
                    print(f'{device_path} metadata:')
                    for key, value in self._meta.items():
                        subtopic = key[len(device_path) + 1:]
                        print(f'  {subtopic} {value}')
                    print(f'\n{device_path} values:')
                for key, value in self._values.items():
                    meta = self._meta.get(key, None)
                    if meta is not None:
                        fmt = meta.get('format', None)
                        if fmt == 'version':
                            value = version_to_str(value)
                    if args.verbose:
                        subtopic = key[len(device_path) + 1:]
                        print(f'  {subtopic} = {value}')
                    else:
                        print(f'{key} = {value}')
        return 0


def on_cmd(args):
    return Info(args.device_path).run(args)
