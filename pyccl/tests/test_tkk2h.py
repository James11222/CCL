import numpy as np
import pytest
import pyccl as ccl


COSMO = ccl.Cosmology(
    Omega_c=0.27, Omega_b=0.045, h=0.67, sigma8=0.8, n_s=0.96,
    transfer_function='bbks', matter_power_spectrum='linear')
M200 = ccl.halos.MassDef200m()
HMF = ccl.halos.MassFuncTinker10(COSMO, mass_def=M200)
HBF = ccl.halos.HaloBiasTinker10(COSMO, mass_def=M200)
P1 = ccl.halos.HaloProfileNFW(ccl.halos.ConcentrationDuffy08(M200),
                              fourier_analytic=True)
P2 = ccl.halos.HaloProfileHOD(ccl.halos.ConcentrationDuffy08(M200))
P3 = ccl.halos.HaloProfilePressureGNFW()
P4 = P1
Pneg = ccl.halos.HaloProfilePressureGNFW(P0=-1)
PKC = ccl.halos.Profile2pt()
Prof3pt = ccl.halos.Profile3pt()
PKCH = ccl.halos.Profile2ptHOD()
KK = np.geomspace(1E-3, 10, 32)
MM = np.geomspace(1E11, 1E15, 16)
AA = 1.0


def smoke_assert_tkk2h_real(func):
    sizes = [(0, 0),
             (2, 0),
             (0, 2),
             (2, 3),
             (1, 3),
             (3, 1)]
    shapes = [(),
              (2,),
              (2, 2,),
              (2, 3, 3),
              (1, 3, 3),
              (3, 1, 1)]
    for (sa, sk), sh in zip(sizes, shapes):
        if sk == 0:
            k = 0.1
        else:
            k = np.logspace(-2., 0., sk)
        if sa == 0:
            a = 1.
        else:
            a = np.linspace(0.5, 1., sa)
        p = func(k, a)
        assert np.shape(p) == sh
        assert np.all(np.isfinite(p))


@pytest.mark.parametrize('pars',
                         [{'p1': P1, 'p2': None, 'p3': None, 'p4': None,
                           'cv13': None,  'cv14': None, 'cv24': None, 'cv32':
                           None, 'norm': False},
                          {'p1': P1, 'p2': None, 'p3': None, 'p4': None,
                           'cv13': None,  'cv14': None, 'cv24': None, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': None, 'p4': None,
                           'cv13': None,  'cv14': None, 'cv24': None, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': None, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': None, 'p3': None, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': None, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': PKCH, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': None, 'cv24': PKCH, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': None, 'cv24': PKC, 'cv32':
                           None, 'norm': True},
                           {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': PKC, 'cv24': PKC, 'cv32':
                           PKCH, 'norm': True},
                          ])
def test_tkk2h_22_smoke(pars):
    hmc = ccl.halos.HMCalculator(COSMO, HMF, HBF, mass_def=M200,
                                 nlog10M=2)

    def f(k, a):
        return ccl.halos.halomod_trispectrum_2h_22(COSMO, hmc, k, a,
                                                prof1=pars['p1'],
                                                prof2=pars['p2'],
                                                prof3=pars['p3'],
                                                prof4=pars['p4'],
                                                prof13_2pt=pars['cv13'],
                                                prof14_2pt=pars['cv14'],
                                                prof24_2pt=pars['cv24'],
                                                prof32_2pt=pars['cv32'],
                                                normprof1=pars['norm'],
                                                normprof2=pars['norm'],
                                                normprof3=pars['norm'],
                                                normprof4=pars['norm'],
                                                p_of_k_a=None)
    smoke_assert_tkk2h_real(f)


@pytest.mark.parametrize('pars',
                         [{'p1': P1, 'p2': None, 'p3': None, 'p4': None,
                           'cv13': None, 'cv14': None, 'cv24': None,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': False},
                          {'p1': P1, 'p2': None, 'p3': None, 'p4': None,
                           'cv13': None,  'cv14': None, 'cv24': None,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': None, 'p4': None,
                           'cv13': None,  'cv14': None, 'cv24': None,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': None,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': None, 'p3': None, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': None,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': None,  'cv14': None, 'cv24': PKCH,
                           'cv32': None, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': PKC, 'cv24': PKCH,
                           'cv32': PKC, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': PKC, 'cv24': PKCH,
                           'cv32': PKC, 'cv234': Prof3pt, 'cv134': None,
                           'cv124': None, 'cv123': None, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': PKC, 'cv24': PKCH,
                           'cv32': PKC, 'cv234': None, 'cv134': None,
                           'cv124': None, 'cv123': Prof3pt, 'norm': True},
                          {'p1': P1, 'p2': P2, 'p3': P3, 'p4': P4,
                           'cv13': PKC,  'cv14': PKC, 'cv24': PKCH,
                           'cv32': PKC, 'cv234': Prof3pt, 'cv134': Prof3pt,
                           'cv124': Prof3pt, 'cv123': Prof3pt, 'norm': True},
                          ])
def test_tkk2h_13_smoke(pars):
    hmc = ccl.halos.HMCalculator(COSMO, HMF, HBF, mass_def=M200,
                                 nlog10M=2)

    def f(k, a):
        return ccl.halos.halomod_trispectrum_2h_13(COSMO, hmc, k, a,
                                                prof1=pars['p1'],
                                                prof2=pars['p2'],
                                                prof3=pars['p3'],
                                                prof4=pars['p4'],
                                                prof234_3pt=pars['cv234'],
                                                prof134_3pt=pars['cv134'],
                                                prof124_3pt=pars['cv124'],
                                                prof123_3pt=pars['cv123'],
                                                normprof1=pars['norm'],
                                                normprof2=pars['norm'],
                                                normprof3=pars['norm'],
                                                normprof4=pars['norm'],
                                                p_of_k_a=None)
    smoke_assert_tkk2h_real(f)


def test_Tk3D_2h():
    hmc = ccl.halos.HMCalculator(COSMO, HMF, HBF, mass_def=M200)
    k_arr = KK
    a_arr = np.array([0.1, 0.4, 0.7, 1.0])
    tkk_arr = ccl.halos.halomod_trispectrum_2h_22(COSMO, hmc, k_arr, a_arr,
                                                  P1, prof2=P2,
                                                  prof3=P3, prof4=P4,
                                                  prof13_2pt=PKC,
                                                  prof14_2pt=PKC,
                                                  prof24_2pt=PKC,
                                                  prof32_2pt=PKC,
                                                  normprof1=True,
                                                  normprof2=True,
                                                  normprof3=True,
                                                  normprof4=True,
                                                  p_of_k_a=None)

    tkk_arr += ccl.halos.halomod_trispectrum_2h_13(COSMO, hmc, k_arr, a_arr,
                                                   prof1=P1, prof2=P2,
                                                   prof3=P3, prof4=P4,
                                                   prof234_3pt=None,
                                                   prof134_3pt=None,
                                                   prof124_3pt=None,
                                                   prof123_3pt=None,
                                                   normprof1=True,
                                                   normprof2=True,
                                                   normprof3=True,
                                                   normprof4=True,
                                                   p_of_k_a=None)


    # Input sampling
    tk3d = ccl.halos.halomod_Tk3D_2h(COSMO, hmc,
                                     P1, prof2=P2,
                                     prof3=P3, prof4=P4,
                                     prof13_2pt=PKC,
                                     prof14_2pt=PKC,
                                     prof24_2pt=PKC,
                                     prof32_2pt=PKC,
                                     prof234_3pt=None,
                                     prof134_3pt=None,
                                     prof124_3pt=None,
                                     prof123_3pt=None,
                                     normprof1=True,
                                     normprof2=True,
                                     normprof3=True,
                                     normprof4=True,
                                     p_of_k_a=None,
                                     lk_arr=np.log(k_arr),
                                     a_arr=a_arr,
                                     use_log=True)
    tkk_arr_2 = np.array([tk3d.eval(k_arr, a) for a in a_arr])
    assert np.all(np.fabs((tkk_arr / tkk_arr_2 - 1)).flatten()
                  < 1E-4)

    # Standard sampling
    tk3d = ccl.halos.halomod_Tk3D_2h(COSMO, hmc,
                                     P1, prof2=P2,
                                     prof3=P3, prof4=P4,
                                     prof13_2pt=PKC,
                                     prof14_2pt=PKC,
                                     prof24_2pt=PKC,
                                     prof32_2pt=PKC,
                                     prof234_3pt=None,
                                     prof134_3pt=None,
                                     prof124_3pt=None,
                                     prof123_3pt=None,
                                     normprof1=True,
                                     normprof2=True,
                                     normprof3=True,
                                     normprof4=True,
                                     p_of_k_a=None,
                                     lk_arr=np.log(k_arr),
                                     use_log=True)
    tkk_arr_2 = np.array([tk3d.eval(k_arr, a) for a in a_arr])
    assert np.all(np.fabs((tkk_arr / tkk_arr_2 - 1)).flatten()
                  < 1E-4)


# def test_tkk2h_errors():
#     from pyccl.pyutils import assert_warns
#
#     hmc = ccl.halos.HMCalculator(COSMO, HMF, HBF, mass_def=M200)
#     k_arr = KK
#     a_arr = np.array([0.1, 0.4, 0.7, 1.0])
#
#     # Wrong first profile
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr, None)
#     # Wrong other profiles
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr,
#                                          P1, prof2=PKC)
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr,
#                                          P1, prof3=PKC)
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr,
#                                          P1, prof4=PKC)
#     # Wrong 2pts
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr,
#                                          P1, prof12_2pt=P2)
#     with pytest.raises(TypeError):
#         ccl.halos.halomod_trispectrum_1h(COSMO, hmc, k_arr, a_arr,
#                                          P1, prof34_2pt=P2)
#
#     # Negative profile in logspace
#     assert_warns(ccl.CCLWarning, ccl.halos.halomod_Tk3D_1h,
#                  COSMO, hmc, P3, prof2=Pneg,
#                  lk_arr=np.log(k_arr), a_arr=a_arr,
#                  use_log=True)
