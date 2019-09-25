"""Classes for modeling bridges and loads."""
from model.bridge import Point


class Response:
    """A sensor response collected from a simulation."""
    # TODO: Move to fem.response
    def __init__(
            self, value: float, x: float=None, y: float=None, z: float=None,
            time: int=0, elem_id: int=None, srf_id: int=None,
            node_id: int=None, section_id: int=None, fiber_cmd_id: int=None):
        self.value = value
        self.point = Point(x=x, y=y, z=z)
        self.time = time
        self.node_id = node_id
        self.elem_id = elem_id
        self.srf_id = srf_id
        self.section_id = section_id
        self.fiber_cmd_id = fiber_cmd_id

    def __str__(self):
        """Readable representation of a sensor response."""
        str_if = lambda s, b: "" if b else s
        return (f"{self.value}"
               + f" at (x={self.point.x}, y={self.point.y}, z={self.point.z})"
               + f" t={self.time}"
               + str_if(f" node_id={self.node_id}", self.node_id)
               + str_if(f" elem_id={self.elem_id}", self.elem_id)
               + str_if(f" srf_id={self.srf_id}", self.srf_id)
               + str_if(f" section_id={self.section_id}", self.section_id)
               + str_if(f" fiber_cmd_id={self.fiber_cmd_id}",
                        self.fiber_cmd_id))
