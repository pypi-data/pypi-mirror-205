# PyTest will consider all `.py` filenames that begin with `test_` (or end with `_test`) as test files.
# Then it will run all functions with prefix `test_`, which may be inside classes with prefix `Test`, and look for `assert` statements.
# Therefore it is important to put all imports inside the function.
# Also because these test functions are located inside the `test` directory, we need to update the import location with `../src`.
# But this is not a good practice. We should install the package in development mode, and run PyTest against that instead.



# def test_paraview(num_s=21, num_u=30, num_v=78):
# def test_paraview(num_s=21, num_u=10, num_v=39):
def test_paraview(num_s=3, num_u=4, num_v=5):
    """
    Test outputting ParaView files.
    """

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import sys
    basedir = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.join(basedir, '..', 'src')) # Because we are inside './test/' directory.
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO

    # import logging
    from gvec_to_python.util.logger import logger
    # logger = logging.getLogger(__name__)

    import numpy as np

    import vtk
    from gvec_to_python.reader.gvec_reader import GVEC_Reader
    from gvec_to_python.reader.sample_loader import SampleEnum, SampleEquilibrium
    from gvec_to_python.writer.paraview.vtk_writer import vtkWriter
    import gvec_to_python.writer.paraview.mesh_creator as MC
    from gvec_to_python import GVEC, Form, Variable

    logger.info(' ')
    logger.info('='*80)
    logger.info('Running `test_paraview()`.')
    logger.info('Write `.vtk` ParaView files to a local `GVEC/` folder using sample GVEC dataset.')
    logger.info('='*80)
    logger.info(' ')

    logger.info(f'VTK version: {vtk.vtkVersion.GetVTKVersion()}')



    # ============================================================
    # Init GVEC class.
    # ============================================================

    # Old mechanism:
    # filepath = 'GVEC/testcases/ellipstell/'
    # filepath =  os.path.join(basedir, '..', filepath) # Because we are inside './test/' directory.
    # filename = 'GVEC_ellipStell_profile_update_State_0000_00010000.json'
    # gvec = GVEC(filepath, filename)

    # New mechanism, using sample within this repo:
    sample_equilibrium = SampleEquilibrium(SampleEnum.ELLIP_STELL_V2_E1D6_M6N6)
    gvec = sample_equilibrium.get_gvec_object()
    num_s = sample_equilibrium.get_sample_metadata()['Nels'][0] # Override input parameter.
    filepath = sample_equilibrium.get_sample_metadata()['filepath']

    # If user-provided equilibrium:
    # gvec = SampleEquilibrium.get_user_gvec_object(filepath, filename)



    # ============================================================
    # Write data as ParaView .vtu file.
    # ============================================================

    # Output directory.
    # vtk_dir = os.path.join(basedir, 'GVEC')
    vtk_dir = os.path.join(filepath, 'ParaView')

    # Class implementation of a ParaView writer.
    writer = vtkWriter('vtu')

    # Sample points uniformly in (s, u, v) and convert them to (x, y, z).
    # s_range = np.arange(0, 1.0001, 0.1)
    # u_range = np.arange(0, 1.0000, 0.05)  # Skipping the last point because periodic.
    # v_range = np.arange(0, 1.0000, 0.025) # Skipping the last point because periodic.
    periodic = True
    if periodic:
        s_range = np.linspace(0, 1, num_s)
        u_range = np.linspace(0, 1, num_u+1)[:-1] # Skipping the last point because periodic.
        v_range = np.linspace(0, 1, num_v+1)[:-1] # Skipping the last point because periodic.
    else:
        s_range = np.linspace(0, 1, num_s)
        u_range = np.linspace(0, 1, num_u)
        v_range = np.linspace(0, 1, num_v)
    use_GVEC_grid = True
    interpolate_GVEC_grid = True
    interpolate_factor = 4
    assert interpolate_factor >= 1
    if use_GVEC_grid:
        s_range = np.array(gvec.data['grid']['sGrid'])
        if interpolate_GVEC_grid:
            s_range_orig = s_range
            s_range = []
            # Increase elements by 4x. 21 points -> 81 points.
            for i, s in enumerate(s_range_orig):
                if i == len(s_range_orig) - 1:
                    s_range.append(s)
                else:
                    s_range = s_range + np.linspace(s, s_range_orig[i+1], interpolate_factor, endpoint=False).tolist()
            s_range = np.array(s_range)
    bypass_zero = True
    if bypass_zero:
        s_range[0] = 1e-12 # Bypass 0 if it blows up.

    test_cases = []

    # ==========
    # Point
    # ==========
    test_cases.append(
        {
            'filename': 'Test01_Points_Vertex',
            'function': MC.connect_vertex,
            'periodic': None
        }
    )

    # ==========
    # Line
    # ==========
    test_cases.append(
        {
            'filename': 'Test02_Line_Toroidal(periodic)',
            'function': MC.connect_line_toroidal,
            'periodic': True
        }
    )
    test_cases.append(
        {
            'filename': 'Test02_Line_Toroidal(aperiodic)',
            'function': MC.connect_line_toroidal,
            'periodic': False
        }
    )
    test_cases.append(
        {
            'filename': 'Test03_Line_Poloidal',
            'function': MC.connect_line_poloidal,
            'periodic': None
        }
    )
    test_cases.append(
        {
            'filename': 'Test04_Line_Radial',
            'function': MC.connect_line_radial,
            'periodic': None
        }
    )

    # ==========
    # Surface
    # ==========
    test_cases.append(
        {
            'filename': 'Test05_Surface_Angular(periodic)',
            'function': MC.connect_quad_angular,
            'periodic': True
        }
    )
    test_cases.append(
        {
            'filename': 'Test05_Surface_Angular(aperiodic)',
            'function': MC.connect_quad_angular,
            'periodic': False
        }
    )
    test_cases.append(
        {
            'filename': 'Test06_Surface_CrossSection',
            'function': MC.connect_quad_crosssection,
            'periodic': None
        }
    )

    # ==========
    # Volume
    # ==========
    test_cases.append(
        {
            'filename': 'Test07_Volume_Torus(periodic)',
            'function': MC.connect_cell,
            'periodic': True
        }
    )
    test_cases.append(
        {
            'filename': 'Test07_Volume_Torus(aperiodic)',
            'function': MC.connect_cell,
            'periodic': False
        }
    )

    MC.make_ugrid_and_write_vtu(test_cases, writer, vtk_dir, gvec, s_range, u_range, v_range)

    gvec.mapfull.clear_cache()



if __name__ == "__main__":
    test_paraview()
