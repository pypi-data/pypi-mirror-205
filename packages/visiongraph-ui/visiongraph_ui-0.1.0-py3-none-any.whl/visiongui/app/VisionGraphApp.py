import logging
import traceback
from typing import Generic, TypeVar

from open3d.visualization import gui
from typing_extensions import override
from visiongraph import BaseGraph

from visiongui.app.BaseApp import T, BaseApp

G = TypeVar("G", bound=BaseGraph)


class VisionGraphApp(BaseApp[T], Generic[T, G]):
    def __init__(self, config: T, graph: G, width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False, handle_graph_state: bool = True):
        super().__init__(config, graph.name, width, height, attach_interrupt_handler)

        self.graph = graph
        self.graph.on_exception = self._on_graph_exception

        self.handle_graph_state = handle_graph_state
        if self.handle_graph_state:
            self.graph.open()

    def _on_graph_exception(self, pipeline, ex):
        # display error message in console
        logging.warning("".join(traceback.TracebackException.from_exception(ex).format()))

        # close application on graph exception
        gui.Application.instance.post_to_main_thread(self.window, gui.Application.instance.quit)

    @override
    def _on_close(self):
        if self.handle_graph_state:
            self.graph.close()
        gui.Application.instance.quit()
