import os

from gig import Ent, EntType
from matplotlib.patches import Patch

from lk_urban.AbstractUrbanMap import AbstractUrbanMap

_URBAN_LG_TYPES = {"MC", "UC"}


class LocalAuthorityUrbanMap(AbstractUrbanMap):
    def get_ent_type(self) -> EntType:
        return EntType.LG

    def is_urban(self, ent: Ent) -> bool:
        return self._lg_type(ent) in _URBAN_LG_TYPES

    def get_color(self, ent: Ent) -> str:
        return "red" if self._lg_type(ent) == "MC" else "orange"

    def get_title_label(self) -> str:
        return "Urban = Municipal Councils or Urban Councils"

    def get_district_id(self, ent: Ent) -> str:
        return ent.district_id

    def get_image_path(self) -> str:
        return os.path.join("images", f"{self._class_label()}.png")

    def get_legend_handles(self):
        return [
            Patch(facecolor="red", edgecolor="none", label="MC"),
            Patch(facecolor="orange", edgecolor="none", label="UC"),
        ]

    def get_legend_title(self) -> str:
        return "LG Type"

    @staticmethod
    def _lg_type(ent: Ent) -> str:
        return ent.name.split(" ")[-1]
