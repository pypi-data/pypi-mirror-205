from typing import (
    TYPE_CHECKING,
    Type
)
from typing_extensions import Self
from xoa_driver.internals.core.commands import (
    C_REMOTEPORTCOUNTS,
    C_BUILDSTRING,
)
from xoa_driver.internals.utils.modules_manager import ModulesManager
from xoa_driver.internals.hli_v2 import revisions
from xoa_driver.internals import exceptions
if TYPE_CHECKING:
    from xoa_driver.internals.hli_v2.modules import module_l47 as ml47

from xoa_driver.internals.state_storage import testers_state
from ._base_tester import BaseTester
from .genuine import management_interface as mi


def get_module_type(revision: str) -> "Type":
    module_type = revisions.VULCAN_MODULES.get(revision)
    if not module_type:
        raise exceptions.WrongModuleError(
            revision,
            set(revisions.VULCAN_MODULES.keys()),
        )
    return module_type


class L47Tester(BaseTester["testers_state.GenuineTesterLocalState"]):
    """
    Representation of a physical Xena Vulcan Tester.
    """

    def __init__(self, host: str, username: str, password: str = "xena", port: int = 22606, *, debug: bool = False) -> None:
        super().__init__(host=host, username=username, password=password, port=port, debug=debug)

        self._local_states = testers_state.GenuineTesterLocalState(host, port)

        self.build_string = C_BUILDSTRING(self._conn)
        """
        Representation of C_BUILDSTRING
        """

        self.management_interface = mi.ManagementInterface(self._conn)
        """
        Tester management interface that includes IP address, DHCP, MAC address and hostname.
        """

        self.modules: ModulesManager["ml47.ModuleL47"] = ModulesManager(self._conn, get_module_type)
        """
        Module index manager of the tester.
        """

    @property
    def info(self) -> testers_state.GenuineTesterLocalState:
        return self._local_states

    async def _setup(self) -> Self:
        await super()._setup()
        await self._local_states.initiate(self)
        self._local_states.register_subscriptions(self)

        ft_pc = await C_REMOTEPORTCOUNTS(self._conn).get()
        port_counts = ft_pc.port_counts
        await self.modules.fill_l47(port_counts)
        return self
