import os
import re
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from gig import Ent, EntType, GIGTable
from utils import Log

log = Log("AbstractUrbanMap")


class AbstractUrbanMap(ABC):
    def __init__(self):
        self._gig_table = GIGTable("population-ethnicity", "regions", "2012")

    def _class_label(self) -> str:
        name = type(self).__name__.removesuffix("UrbanMap")
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    @abstractmethod
    def get_ent_type(self) -> EntType:
        pass

    @abstractmethod
    def is_urban(self, ent: Ent) -> bool:
        pass

    @abstractmethod
    def get_title_label(self) -> str:
        pass

    def get_title(self, p_urban: float) -> str:
        return f"{self.get_title_label()}\n({p_urban:.1%} of population)"

    @abstractmethod
    def get_image_path(self) -> str:
        pass

    def get_population(self, ent: Ent) -> int:
        return ent.gig(self._gig_table).total

    def get_color(self, ent: Ent) -> str:
        return "red"

    def get_legend_handles(self):
        return None

    def get_legend_title(self) -> str | None:
        return None

    def _draw_districts(self, ax):
        districts = Ent.list_from_type(EntType.DISTRICT)
        for district in districts:
            district.geo().plot(
                ax=ax, color="white", edgecolor="lightgray", linewidth=0.5
            )

    def _draw_ents(self, ax) -> tuple[int, int]:
        ents = Ent.list_from_type(self.get_ent_type())
        pop_total, pop_urban = 0, 0
        for ent in ents:
            try:
                population = self.get_population(ent)
                if self.is_urban(ent):
                    ent.geo().plot(
                        ax=ax, color=self.get_color(ent), edgecolor="none"
                    )
                    pop_urban += population
                pop_total += population
            except Exception as e:
                log.error(f"Error processing {ent.name}: {e}")
        return pop_total, pop_urban

    def _configure_axes(self, ax, p_urban: float):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_frame_on(False)
        plt.title(self.get_title(p_urban), wrap=True)
        legend_handles = self.get_legend_handles()
        if legend_handles:
            ax.legend(handles=legend_handles, title=self.get_legend_title())

    def _save_figure(self):
        image_path = self.get_image_path()
        os.makedirs(os.path.dirname(image_path) or ".", exist_ok=True)
        plt.savefig(image_path, dpi=300)
        log.info(f'Wrote "{image_path}"')
        plt.close()

    def render(self):
        _fig, ax = plt.subplots(figsize=(5, 5))
        self._draw_districts(ax)
        pop_total, pop_urban = self._draw_ents(ax)
        p_urban = pop_urban / pop_total if pop_total else 0
        log.info(f"Total population: {pop_total:,}")
        log.info(f"Urban population: {pop_urban:,}")
        log.info(f"Proportion of urban population: {p_urban:.1%}")
        self._configure_axes(ax, p_urban)
        self._save_figure()
