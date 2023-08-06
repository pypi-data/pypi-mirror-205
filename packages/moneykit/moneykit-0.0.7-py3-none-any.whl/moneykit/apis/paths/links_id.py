from moneykit.paths.links_id.delete import ApiFordelete
from moneykit.paths.links_id.get import ApiForget
from moneykit.paths.links_id.patch import ApiForpatch


class LinksId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
