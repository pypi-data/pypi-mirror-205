"""
A Python driver for Sartorius and Minebea Intec ethernet scales.

Distributed under the GNU General Public License v2
Copyright (C) 2019 NuMat Technologies
"""
import logging

from sartorius.util import TcpClient

logger = logging.getLogger('sartorius')


class Scale(TcpClient):
    """Driver for Sartorius and Minebea Intec ethernet scales.

    This implements a version of the Scale Manufacturers Association
    standardized communications protocol.
    """

    def __init__(self, ip: str, port: int = 49155) -> None:
        """Set up connection parameters, IP address and port."""
        self.units: str = ""
        if ":" in ip:
            port = int(ip.split(":")[1])
            ip = ip.split(':')[0]
        super().__init__(ip, port)

    async def get(self) -> dict:
        """Get scale reading."""
        response = await self._write_and_read('\x1bP')
        if not response:
            raise OSError("Unable to get reading from scale.")
        return self._parse(response)

    async def get_info(self) -> dict:
        """Get scale model, serial, and software version numbers."""
        model = await self._write_and_read('\x1bx1_')
        serial = await self._write_and_read('\x1bx2_')
        software = await self._write_and_read('\x1bx3_')
        if not (model and serial and software):
            raise OSError("Unable to get information from scale.")
        response = {
            'model': model.strip(),
            'serial': serial.strip(),
            'software': software.strip(),
        }
        for item in response.values():
            if (' + ' in item or ' kg' in item):
                logger.error(f"Received malformed data: {response}")
                return {}
        return response

    async def zero(self) -> None:
        """Tare and zero the scale."""
        await self._write_and_read('\x1bT')

    def _parse(self, response: str) -> dict:
        """Parse a scale response.

        Scale weight is returned according to the SMA communication standard:
            K K K K K K + * A A A A A A A A * E E E CR LF
        K: ID code character
        +: plus or minus
        *: space
        A: Digit or letter
        E: unit symbol

        Errors are similar:
            S t a t * * * * * E r r * * # # * * * * CR LF
        #: Error code number
        The most common is "Stat       OFF", indicating the unit is plugged in
        but the face plate is off.

        One weird behavior is in the units field. This field is empty when the
        scale is unstable (weight shifting) but filled in when the reading is
        stable. This implementation converts that to a "stable" boolean.
        """
        if response is None:
            return {'on': False}
        elif len(response) != 22:
            logger.error(f"Received malformed data: {response}")
            return {'on': False}
        id = response[:6].strip()
        if id == 'Stat':
            error = response[9:14].strip()
            logger.warning(f'Could not read: {error}')
            return {'on': False}
        elif id != 'N':
            raise ValueError("This driver only supports net weight.")
        mass = float(response[6:16].replace(' ', ''))
        units = response[17:20].strip()
        if units:
            self.units = units
            stable = True
        else:
            units = self.units
            stable = False
        return {
            'mass': mass,
            'units': units,
            'stable': stable,
        }
