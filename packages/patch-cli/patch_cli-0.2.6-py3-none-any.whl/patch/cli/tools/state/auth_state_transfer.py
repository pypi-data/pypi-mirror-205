from patch.cli.tools.state.bi_directional_state_transfer import BiDirectionalStateTransfer
from patch.storage.domain import get_patch_domain


class AuthStateTransfer(BiDirectionalStateTransfer):
    def __init__(self, path, path_poll):
        super().__init__(get_patch_domain(), path, path_poll)
