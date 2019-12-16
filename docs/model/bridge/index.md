Module model.bridge
===================
Model of a bridge.

Sub-modules
-----------
* model.bridge.bridge_705
* model.bridge.test_bridge
* model.bridge.util

Classes
-------

`Bridge(name, accuracy, length, width, supports, sections, lanes, dimensions, base_mesh_deck_nodes_x, base_mesh_deck_nodes_z, base_mesh_pier_nodes_y, base_mesh_pier_nodes_z, nodes_at_mat_props=False, single_sections=None)`
:   A bridge specification.
    
    Args:
        name: str, the name of the bridge.
        length: float, length of the bridge in meters.
        width: float, width of the bridge in meters.
        supports: List[Support], a list of supports in 2D or 3D.
        sections: List[Section], the bridge's cross section in 2D or 3D.
        lanes: List[Lane], lanes that span the bridge, where to place loads.
        dimensions: Dimensions, whether the model is 2D or 3D.
        base_mesh_deck_nodes_x: int, number of nodes of the base mesh in
            longitudinal direction of the bridge deck, minimum is 2.
        base_mesh_deck_nodes_z: Optional[int], number of nodes of the base mesh
            in transverse direction of the bridge deck, minimum is 2.
        base_mesh_pier_nodes_y: Optional[int], number of nodes of the base mesh
            in vertical direction of the piers, minimum is 2.
        base_mesh_pier_nodes_z: Optional[int], number of nodes of the base mesh
            in transverse direction of the piers, minimum is 2.
        single_sections: Optional[Tuple[Section, Section]], if given then
            override the bridge's deck and each pier sections with the given
            values respectively in the tuple, only applies to a 3D model.

    ### Methods

    `deck_section_at(self, x, z)`
    :   Return the deck section at given position.

    `id_str(self, acc=True)`
    :   Name with dimensions attached.
        
        Args:
            acc: bool, whether to include (True) or ignore bridge accuracy.

    `print_info(self, pier_fix_info=False)`
    :   Print summary information about this bridge.
        
        Args:
            fix_info: print information on pier's fixed nodes.

    `wheel_tracks(self, c)`
    :   Z positions of wheel track on the bridge.

    `x(self, x_frac)`
    :

    `x_axis(self)`
    :   Position of supports in meters along the bridge's x-axis.

    `x_axis_equi(self, n)`
    :   n equidistant values along the bridge's x-axis, in meters.

    `x_frac(self, x)`
    :

    `y(self, y_frac)`
    :

    `y_frac(self, y)`
    :

    `y_min_max(self)`
    :   The min and max values in y direction from supports and sections.

    `z(self, z_frac)`
    :

    `z_frac(self, z)`
    :

    `z_min_max(self)`
    :   The min and max values in z direction from supports and sections.

`Dimensions(*args, **kwargs)`
:   Whether modeling in 2D or 3D.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `D2`
    :   Whether modeling in 2D or 3D.

    `D3`
    :   Whether modeling in 2D or 3D.

    ### Methods

    `name(self)`
    :

`Fix(x_frac, x=False, y=False, z=False, rot=False)`
:   A node fixed in some degrees of freedom, when 2D modeling.
    
    Args:
        x_frac: float, fraction of x position in [0 1].
        x: bool, whether to fix x translation.
        y: bool, whether to fix y translation.
        rot: bool, whether to fix rotation.
    
    TODO: Rename to Support2D and move to absolute position.

    ### Methods

    `y_min_max(self)`
    :   The min and max values in y direction for this support.

    `z_min_max(self)`
    :   The min and max values in z direction for this support.

`Lane(z0, z1, ltr)`
:   A traffic lane spanning the length of a bridge.
    
    Args:
        z0: float, z ordinate of one edge of the lane in meters.
        z1: float, z ordinate of the other edge of the lane in meters.
        ltr: bool, whether traffic moves left to right, or opposite.
    
    Attrs:
        z_min, float, lower z position of the bridge in meters.
        z_min, float, upper z position of the bridge in meters.
        width, float, Width of the lane in meters.

`Layer(y_min, z_min, y_max, z_max, num_fibers, area_fiber=0.00049, material=Material.Steel)`
:   A straight line of fibers when describing a Section, when 2D modeling.
    
    Args:
        y_i, z_i: float, y and z positions in meters of the first fiber.
        y_j, z_j: float, y and z positions in meters of the last fiber.
        num_fibers: int, number of fibers along the line.
        area_fiber: float, area of each fiber.
        material: Material, material of the fibers.
    
    TODO: Avoid default argument of area_fiber.

    ### Methods

    `points(self)`
    :   The points representing each fiber.

`Material(*args, **kwargs)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Concrete`
    :   An enumeration.

    `Steel`
    :   An enumeration.

`Patch(y_min, z_min, y_max, z_max, num_sub_div_z=30, material=Material.Concrete)`
:   A rectangular patch when describing a Section, when 2D modeling.

    ### Methods

    `points(self)`
    :   Points for the center of each subdivision, starting at min z.

`Point(x=0, y=0, z=0)`
:   A point described by three positions in meters: (x, y, z).
    
    X is along the deck, y is the height, and z is across the deck.
    
    TODO: Change default arguments to None.

    ### Methods

    `distance(self, point)`
    :

`Section2D(patches=[], layers=[])`
:   A section when 2D modeling, composed of fibers (Patch and Layer).

    ### Class variables

    `next_id`
    :   int([x]) -> integer
        int(x, base=10) -> integer
        
        Convert a number or string to an integer, or return 0 if no arguments
        are given.  If x is a number, return x.__int__().  For floating point
        numbers, this truncates towards zero.
        
        If x is not a number or if base is given, then x must be a string,
        bytes, or bytearray instance representing an integer literal in the
        given base.  The literal can be preceded by '+' or '-' and be surrounded
        by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
        Base 0 means to interpret the base from the string as an integer literal.
        >>> int('0b100', base=0)
        4

    ### Methods

    `y_min_max(self)`
    :   The min and max values in y for this section.

    `z_min_max(self)`
    :   The min and max values in z for this section.

`Section3D(density, thickness, youngs, poissons, start_x_frac, start_z_frac, end_x_frac, end_z_frac)`
:   A section for describing the deck when 3D modeling.
    
    Args:
        density: float, section density in kg/m.
        thickness: float, section thickness in m.
        youngs: float, Young's modulus of the section in MPa.
        poisson: float, Poisson's ratio.
        start_x_frac: float, start of the section as a fraction of x position.
        start_z_frac: float, start of the section as a fraction of z position.
        end_x_frac: float, end of the section as a fraction of x position.
        end_z_frac: float, end of the section as a fraction of z position.

    ### Descendants

    * model.bridge.Section3DPier

    ### Class variables

    `next_id`
    :   int([x]) -> integer
        int(x, base=10) -> integer
        
        Convert a number or string to an integer, or return 0 if no arguments
        are given.  If x is a number, return x.__int__().  For floating point
        numbers, this truncates towards zero.
        
        If x is not a number or if base is given, then x must be a string,
        bytes, or bytearray instance representing an integer literal in the
        given base.  The literal can be preceded by '+' or '-' and be surrounded
        by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
        Base 0 means to interpret the base from the string as an integer literal.
        >>> int('0b100', base=0)
        4

    ### Methods

    `contains(self, bridge, x, z)`
    :   Whether this section contains the given point.

    `mat_id_str(self)`
    :   Representation of this section by material properties.

    `y_min_max(self)`
    :   The min and max values in y for this section.

`Section3DPier(density, thickness, youngs, poissons, start_frac_len)`
:   Like Section3D but intended for describing piers.
    
    Args:
        density: float, section density in kg/m.
        thickness: float, section thickness in m.
        youngs: float, Young's modulus of the section in MPa.
        poisson: float, Poisson's ratio.
        start_frac_len: start of the section as a fraction of pier length.

    ### Ancestors (in MRO)

    * model.bridge.Section3D

`Support3D(x, z, length, height, width_top, width_bottom, sections, fix_x_translation=True, fix_y_translation=True, fix_z_translation=True, fix_x_rotation=False, fix_y_rotation=False, fix_z_rotation=False)`
:   A support of the bridge deck, when 3D modeling.
    
        SIDE_VIEW:
        <------------x----------->
                           <---length-->
        |------------------|-----------|----------------------| ↑ h
                            \         /                         | e
                             \       /                          | i
                              \     /                           | g
                               \   /                            | h
                                \ /                             ↓ t
    
        TOP_VIEW:
        |-----------------------------------------------------| ↑+
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| 0
        |------------------|-----------|----------------------| |
        |------------------|-----------|----------------------| | z = -2
        |------------------|-----------|----------------------| |
        |-----------------------------------------------------| ↓-
    
        FRONT_VIEW:
                           <---width-top---->
                           |----------------|
                            \              /
                             \            /
                              \          /
                               \        /
                                \______/
                                <------>
                              width-bottom
    
    Args:
        x: float, x position of center of the support in meters.
        z: float, z position of center of the support in meters.
        length: float, length of the support in meters.
        height: float, height of the support in meters.
        width_top: float, width of the top of the support in meters.
        width_bottom: float, width of the bottom of the support in meters.

    ### Methods

    `x_min_max(self)`
    :   The min and max x positions for this pier.

    `y_min_max(self)`
    :   The min and max y positions for this pier.

    `z_min_max_top(self)`
    :   The min and max z positions for the top of this pier.