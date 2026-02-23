import os

from gig import Ent, EntType

from lk_urban.AbstractUrbanMap import AbstractUrbanMap


class DensityUrbanMap(AbstractUrbanMap):
    def __init__(
        self,
        ent_type: EntType = EntType.GND,
        density_threshold: int = 1500,
    ):
        super().__init__()
        self.ent_type = ent_type
        self.density_threshold = density_threshold

    def get_ent_type(self) -> EntType:
        return self.ent_type

    def is_urban(self, ent: Ent) -> bool:
        population = ent.gig(self._gig_table).total
        area = ent.area_sqkm
        density = population / area if area else 0
        return density > self.density_threshold

    def get_title_label(self) -> str:
        return (
            f"Areas with population density"
            f" > {self.density_threshold:,}/km²"
        )

    def get_image_path(self) -> str:
        label = self._class_label()
        threshold = self.density_threshold
        ent_name = self.ent_type.name
        return os.path.join("images", f"{label}_{threshold}_{ent_name}.png")
