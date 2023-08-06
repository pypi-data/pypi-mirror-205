# PyTest will consider all `.py` filenames that begin with `test_` (or end with `_test`) as test files.
# Then it will run all functions with prefix `test_`, which may be inside classes with prefix `Test`, and look for `assert` statements.
# Therefore it is important to put all imports inside the function.
# Also because these test functions are located inside the `test` directory, we need to update the import location with `../src`.
# But this is not a good practice. We should install the package in development mode, and run PyTest against that instead.



def test_blown_up_B(plot=False, num_s=123, num_u=2, num_v=2):
    """
    Test the behavior of components of B when s tends to 0.
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
    import matplotlib.pyplot as plt

    from gvec_to_python import GVEC, Form, Variable

    logger.info(' ')
    logger.info('='*80)
    logger.info('Running `test_blown_up_B()`.')
    logger.info('Test the behavior of components of B when s tends to 0.')
    logger.info('When s -> 0, B2_i is expected to decrease at the same rate as Det towards 0.')
    logger.info('='*80)
    logger.info(' ')



    # ============================================================
    # Init GVEC class.
    # ============================================================

    filepath = 'GVEC/testcases/ellipstell/'
    filepath =  os.path.join(basedir, '..', filepath) # Because we are inside './test/' directory.
    filename = 'GVEC_ellipStell_profile_update_State_0000_00010000.json'
    gvec = GVEC(filepath, filename)



    # ============================================================
    # Test various MHD variables and p-forms.
    # ============================================================

    variable=Variable.B
    form=Form.PHYSICAL

    # ============================================================
    # Test grid.
    # ============================================================

    # s_range = np.linspace(0, 1, num_s)
    max_s = 1
    s_range = np.linspace(1e-8, max_s, num_s) # Skip 0 in the plotting step.
    u_range = np.linspace(0, 1, num_u, endpoint=False)
    v_range = np.linspace(0, 1, num_v, endpoint=False)
    logger.info('Total number of points: {}'.format(s_range.shape[0] * u_range.shape[0] * v_range.shape[0]))
    logger.info(' ')



    # ============================================================
    # Test variable: 1D arrays before meshgrid.
    # ============================================================

    # enumerate_input_types(gvec, variable=Variable.B, form=Form.PHYSICAL)
    # enumerate_input_types(gvec, variable=Variable.B, form=Form.CONTRAVARIANT)
    # enumerate_input_types(gvec, variable=Variable.B, form=Form.ONE)
    # enumerate_input_types(gvec, variable=Variable.B, form=Form.TWO)

    Bcv, Bcv_iota, B2, B2_iota, det, J, iota, phi, chi, dphi_ds, dchi_ds, dlambda_dtheta, dlambda_dzeta = eval_B(s_range, u_range, v_range, gvec, form=Form.CONTRAVARIANT)

    logger.info('Bcv.shape : {}'.format(Bcv.shape))
    logger.info('B2.shape  : {}'.format(B2.shape))
    logger.info('det.shape : {}'.format(det.shape))
    logger.info('J.shape   : {}'.format(J.shape))
    logger.info('dchi_ds.shape : {}'.format(dchi_ds.shape))
    logger.info('dphi_ds.shape : {}'.format(dphi_ds.shape))
    logger.info('dlambda_dtheta.shape : {}'.format(dlambda_dtheta.shape))
    logger.info('dlambda_dzeta.shape  : {}'.format(dlambda_dzeta.shape))

    B2_1,   B2_2,   B2_3   = B2       # 2-form = Before division by determinant.
    B2i_s,  B2i_u,  B2i_v  = B2_iota  # 2-form computed using iota.
    Bcv_s,  Bcv_u,  Bcv_v  = Bcv      # Contravariant form.
    Bcvi_s, Bcvi_u, Bcvi_v = Bcv_iota # Contravariant form computed using iota.

    logger.info(' ')
    logger.info('Test implementation B-field.')
    logger.info('B2_i is expected to decrease at the same rate as Det towards s -> 0.')
    logger.info('| {: <4} | {: <11} | {: <11} | {: <11} | {: <13} |'.format(' s', '   Bcv_u', ' B2_2 / det', '   B2_2', '     Det'))
    # Loop over `u` component.
    for i in range(s_range.shape[0]):
        if i > 0:
            logger.info('| {:.2f} | {:+.8f} | {:+.8f} | {:+.8f} | {:+13.8f} |'.format(s_range[i], Bcv_u[i,0,0], B2_2[i,0,0] / det[i,0,0], B2_2[i,0,0], det[i,0,0]))
    logger.info('| {: <4} | {: <11} | {: <11} | {: <11} | {: <13} |'.format(' s', '   Bcv_u', ' B2_2 / det', '   B2_2', '     Det'))
    logger.info(' ')
    logger.info('| {: <4} | {: <11} | {: <11} | {: <11} | {: <13} |'.format(' s', '   Bcv_v', ' B2_3 / det', '   B2_3', '     Det'))
    # Loop over `v` component.
    for i in range(s_range.shape[0]):
        if i > 0:
            logger.info('| {:.2f} | {:+.8f} | {:+.8f} | {:+.8f} | {:+13.8f} |'.format(s_range[i], Bcv_v[i,0,0], B2_3[i,0,0] / det[i,0,0], B2_3[i,0,0], det[i,0,0]))
    logger.info('| {: <4} | {: <11} | {: <11} | {: <11} | {: <13} |'.format(' s', '   Bcv_v', ' B2_3 / det', '   B2_3', '     Det'))
    logger.info(' ')


    # Compute rate of convergence.
    order_q = 1
    mu_det  = (    det[0:-1,:,:] -     det[0,:,:]) / (    det[1:,:,:] -     det[0,:,:])**order_q
    mu_dphi = (dphi_ds[0:-1,:,:] - dphi_ds[0,:,:]) / (dphi_ds[1:,:,:] - dphi_ds[0,:,:])**order_q

    # Order estimation
    q_est_det  = (    det[:-2,:,:] -     det[1:-1,:,:]) / (    det[1:-1,:,:] -     det[2:,:,:]) # 2 elements shorter.
    q_est_dphi = (dphi_ds[:-2,:,:] - dphi_ds[1:-1,:,:]) / (dphi_ds[1:-1,:,:] - dphi_ds[2:,:,:]) # 2 elements shorter.
    q_est_det  = np.log(np.abs(q_est_det))
    q_est_dphi = np.log(np.abs(q_est_dphi))
    q_est_det  = q_est_det[:-1] / q_est_det[1:]   # 3 elements shorter.
    q_est_dphi = q_est_dphi[:-1] / q_est_dphi[1:] # 3 elements shorter.



    plt.rcParams.update({'font.size': 24})
    fig_w = 1280*2
    fig_h = 720*2
    dpi   = 100
    fig, axes = plt.subplots(1, 2, figsize=(fig_w/dpi,fig_h/dpi), dpi=dpi, squeeze=False)

    axes[0,0].set_title('$B^0_u = B^2_2 / det(J) = [\\frac{{d\chi}}{{ds}} - \\frac{{\partial \lambda}}{{\partial \zeta}} * \\frac{{d\phi}}{{ds}}] / det(J) = [(\iota(s) - \\frac{{\partial \lambda}}{{\partial \zeta}}) * \\frac{{d\phi}}{{ds}}] / det(J)$')
    axes[0,1].set_title('$B^0_v = B^2_3 / det(J) = [(1 + \\frac{{\partial \lambda}}{{\partial \\theta}}) * \\frac{{d\phi}}{{ds}}] / det(J)$')
    axes[0,0].plot(s_range[:], Bcv_u[:,0,0],  lw=3, label='$B^0_u (=B^2_2/det)${}'.format(''), marker='x', ms=12)
    axes[0,0].plot(s_range[:], Bcvi_u[:,0,0], lw=3, label='$B^0_u (=B^2_2/det)$ from $\iota(s)${}'.format(''), ls='None', marker='o')
    axes[0,0].plot(s_range[:], B2_2[:,0,0],   lw=3, label='$B^2_2$ (Before 1/det){}'.format(''))
    axes[0,1].plot(s_range[:], Bcv_v[:,0,0],  lw=3, label='$B^0_v (=B^2_2/det)${}'.format(''), marker='x', ms=12)
    axes[0,1].plot(s_range[:], Bcvi_v[:,0,0], lw=3, label='$B^0_v (=B^2_2/det)${} from $\iota(s)$'.format(''), ls='None', marker='o')
    axes[0,1].plot(s_range[:], B2_3[:,0,0],   lw=3, label='$B^2_3$ (Before 1/det){}'.format(''))

    axes[0,0].plot(s_range[:], dlambda_dzeta[:,0,0],                                   lw=3, ls='dotted', label='$\\frac{{\partial \lambda}}{{\partial \zeta}}${}'.format(''))
    axes[0,0].plot(s_range[:], dchi_ds[:,0,0] / dphi_ds[:,0,0] - dlambda_dzeta[:,0,0], lw=3, ls='dotted', label='$\\frac{{d\chi}}{{ds}} / \\frac{{d\phi}}{{ds}} - \\frac{{\partial \lambda}}{{\partial \zeta}} \ (= \iota(s) - \\frac{{\partial \lambda}}{{\partial \zeta}})${}'.format(''))
    # axes[0,0].plot(s_range[:], dchi_ds[:,0,0] - dlambda_dzeta[:,0,0] * dphi_ds[:,0,0], lw=3, ls='dotted', label='$\\frac{{d\chi}}{{ds}} - \\frac{{\partial \lambda}}{{\partial \zeta}} * \\frac{{d\phi}}{{ds}}${}'.format(''))

    axes[0,1].plot(s_range[:],     dlambda_dtheta[:,0,0], lw=3, ls='dotted', label='$\\frac{{\partial \lambda}}{{\partial \\theta}}${}'.format(''))
    axes[0,1].plot(s_range[:], 1 + dlambda_dtheta[:,0,0], lw=3, ls='dotted', label='$1 + \\frac{{\partial \lambda}}{{\partial \\theta}}${}'.format(''))

    for axe in axes:
        for ax in axe:
            ax.set_xlabel('s')
            ax.set_ylabel('Magnitude')
            ax.set_xlim(0,max_s)
            ax.set_ylim(-2,2)
            ax.plot(s_range[:],     det[:,0,0], lw=3, label='$det(J)${}'.format(''), ls='None', marker='o')
            ax.plot(s_range[:],     phi[:,0,0], lw=3, ls='--', label='$\phi(s)${}'.format(''))
            ax.plot(s_range[:],     chi[:,0,0], lw=3, ls='--', label='$\chi(s)${}'.format(''))
            ax.plot(s_range[:],    iota[:,0,0], lw=3, ls='--', label='$\iota(s)${}'.format(''))
            ax.plot(s_range[:], dchi_ds[:,0,0], lw=3, ls='--', label='$\\frac{{d\chi}}{{ds}}${}'.format(''))
            ax.plot(s_range[:], dphi_ds[:,0,0], lw=3, ls='--', label='$\\frac{{d\phi}}{{ds}}${}'.format(''))
            ax.plot(s_range[:-3],  q_est_det[:,0,0], lw=3, label='Convergence order $q_{{det}}${}'.format(''),                       ls='None', marker='1')
            ax.plot(s_range[:-3], q_est_dphi[:,0,0], lw=3, label='Convergence order $q_{{\\frac{{d\phi}}{{ds}}}}${}'.format(''),     ls='None', marker='2')
            ax.plot(s_range[:-1],     mu_det[:,0,0], lw=3, label='Rate of convergence $\mu_{{det}}${}'.format(''),                   ls='None', marker='1')
            ax.plot(s_range[:-1],    mu_dphi[:,0,0], lw=3, label='Rate of convergence $\mu_{{\\frac{{d\phi}}{{ds}}}}${}'.format(''), ls='None', marker='2')

    axes[0,0].legend(loc='lower right')
    axes[0,1].legend(loc='lower right')

    fig.tight_layout()
    # fig.savefig('test_blown_up_B.png', dpi=fig.dpi)
    if plot:
        plt.show()

    # Print values at the pole.
    logger.info('Values at the pole:')
    logger.info(f's_range[0]                                                   {s_range[0]    :+21.16f}')
    logger.info(f'det[0,0,0]                                                   {det[0,0,0]    :+21.16f}')
    logger.info(f'phi[0,0,0]                                                   {phi[0,0,0]    :+21.16f}')
    logger.info(f'dphi_ds[0,0,0]                                               {dphi_ds[0,0,0]:+21.16f}')
    logger.info(f'B2_2[0,0,0]                                                  {B2_2[0,0,0]   :+21.16f}')
    logger.info(f'dchi_ds[0,0,0] - dlambda_dzeta[0,0,0] * dphi_ds[0,0,0]       { dchi_ds[0,0,0] - dlambda_dzeta[0,0,0] * dphi_ds[0,0,0]           :+21.16f}')
    logger.info(f'(dchi_ds[0,0,0] - dlambda_dzeta[0,0,0] * dphi_ds[0,0,0])*2pi {(dchi_ds[0,0,0] - dlambda_dzeta[0,0,0] * dphi_ds[0,0,0]) * 2*np.pi:+21.16f}')
    logger.info(' ')

    logger.info('Conclusion from the plot:')
    logger.info('d(Phi)/ds is crucial to cancelling the convergence of det(J) to zero.')
    logger.info('This is because the other prefactors do not converge to zero.')
    logger.info('But d(Phi)/ds is converging too slow (or det(J) too fast).')



def eval_B(s, u, v, gvec, form):

    import numpy as np

    from gvec_to_python import GVEC, Form, Variable

    if isinstance(s, np.ndarray):

        assert isinstance(s, np.ndarray), '1st argument should be of type `np.ndarray`. Got {} instead.'.format(type(s))
        assert isinstance(u, np.ndarray), '2nd argument should be of type `np.ndarray`. Got {} instead.'.format(type(u))
        assert isinstance(v, np.ndarray), '3rd argument should be of type `np.ndarray`. Got {} instead.'.format(type(v))

        # If input coordinates are simple 1D arrays, turn them into a sparse meshgrid.
        # The output will fallthrough to the logic below, which expects a meshgrid input.
        if s.ndim == 1:
            assert s.ndim == u.ndim, '2nd argument has different dimensions than the 1st. Expected {}, got {} instead.'.format(s.ndim, u.ndim)
            assert s.ndim == v.ndim, '3rd argument has different dimensions than the 1st. Expected {}, got {} instead.'.format(s.ndim, v.ndim)
            s, u, v = np.meshgrid(s, u, v, indexing='ij', sparse=True)

    # ============================================================
    # Below should mirror the logic of 
    # GVEC's get_variable() function almost exactly, 
    # but modified to allow us to probe intermediate values.
    # ============================================================

    J = gvec.df(s, u, v)
    det = gvec.df_det_from_J(J)

    # B-field is in contravariant form, a.k.a. vector fields (GVEC Eq. 1.26).
    # i.e. contravariant components with covariant basis.
    # Pay attention to a 2*pi factor, because we are calculating du and dv here, not d(theta) d(zeta)!
    PHIEDGE = gvec.X1_base.eval_profile(1, gvec.phi_coef)
    phi     = gvec.X1_base.eval_profile(s, gvec.phi_coef)
    chi     = gvec.X1_base.eval_profile(s, gvec.chi_coef)
    iota    = gvec.X1_base.eval_profile(s, gvec.iota_coef)
    # dphi    = gvec.X1_base.eval_profile(s, gvec.dphi_coef) # Coefficients not exposed anymore.
    # dchi    = gvec.X1_base.eval_profile(s, gvec.dchi_coef) # Coefficients not exposed anymore.
    dphi    = (PHIEDGE * 2 * s)        # Analytical.
    dchi    = (PHIEDGE * 2 * s) * iota # Analytical.
    dchi_ds = gvec.X1_base.eval_dprofile(s, gvec.chi_coef) # Old method.
    dphi_ds = gvec.X1_base.eval_dprofile(s, gvec.phi_coef) # Old method.
    dlambda_dtheta = gvec.LA_base.eval_suv_du(s, u, v, gvec.LA_coef) / (2 * np.pi)
    dlambda_dzeta  = gvec.LA_base.eval_suv_dv(s, u, v, gvec.LA_coef) / (2 * np.pi)
    B1  = np.zeros_like(dlambda_dzeta)
    # B2  = ( dchi_ds - dlambda_dzeta * dphi_ds ) * 2 * np.pi
    # B3  = ( (1 + dlambda_dtheta)    * dphi_ds ) * 2 * np.pi
    # B2i = ( (iota - dlambda_dzeta)  * dphi_ds ) * 2 * np.pi
    B2  = ( dchi    - dlambda_dzeta * dphi    ) * 2 * np.pi
    B3  = ( (1 + dlambda_dtheta)    * dphi    ) * 2 * np.pi
    B2i = ( (iota - dlambda_dzeta)  * dphi    ) * 2 * np.pi
    evaled_be4_det      = np.array([B1, B2, B3])    # == 2-form!
    evaled_be4_det_iota = np.array([B1, B2i, B3])   # == 2-form!
    evaled_iota         = evaled_be4_det_iota / det # Contravariant form.
    evaled              = evaled_be4_det      / det # Contravariant form.

    if form == Form.ONE or form == Form.COVARIANT:
        G = gvec.G_from_J(J)
        # If `G` is a batch of metric tensors in a meshgrid.
        if G.ndim == 5:
            for i in range(G.shape[0]):
                for j in range(G.shape[1]):
                    for k in range(G.shape[2]):
                        evaled[:, i, j, k] = G[i, j, k] @ evaled[:, i, j, k]
        # If `G` is one metric tensor.
        else:
            evaled = G @ evaled

    elif form == Form.TWO:
        evaled = det * evaled

    elif form == Form.PHYSICAL:
        # If `J` is a batch of metric tensors in a meshgrid.
        if J.ndim == 5:
            for i in range(J.shape[0]):
                for j in range(J.shape[1]):
                    for k in range(J.shape[2]):
                        evaled[:, i, j, k] = J[i, j, k] @ evaled[:, i, j, k]
        # If `J` is one metric tensor.
        else:
            evaled = J @ evaled

    return evaled, evaled_iota, evaled_be4_det, evaled_be4_det_iota, det, J, iota, phi, chi, dphi, dchi, dlambda_dtheta, dlambda_dzeta



if __name__ == "__main__":

    test_blown_up_B(plot=True)
