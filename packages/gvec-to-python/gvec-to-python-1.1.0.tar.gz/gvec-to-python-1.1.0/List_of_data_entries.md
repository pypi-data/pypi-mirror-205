# Complete list of data entries with their size:

| | Variable Name            | Type        | Size                              | Description |
|-|--------------------------|-------------|-----------------------------------|-------------|
|**>**| **General**          ||||
| | `general%nfp`            | INTEGER     | 1                                 | Number of field periods (toroidal periodicity in a stellarator )|
| | `general%hmap`           | INTEGER     | 1                                 | GVEC internal identifier for the mapping h <br> 1: (R,Z,phi), 2: cylinder, 10: knot |
|**>**| **Grid**             ||||
| | `grid%nElems`            | INTEGER     | 1                                 | number of elements in the 1D radial grid (`npoints=nElems+1`) |
| | `grid%sGrid`             | DOUBLE      | `nElems+1`                        | =knot positions of the spline[^FN-spline], without repetition at the boundary<br>  to have clamped splines |
|**>**| **3D variable** (`..`=`X1` / `X2` / `LA`) ||||
| | `..%s_base%nBase`        | INTEGER     | 1                                 | Spline-base: Number of basis functions |
| | `..%s_base%deg`          | INTEGER     | 1                                 | Spline-base: degree |
| | `..%s_base%continuity`   | INTEGER     | 1                                 | Spline-base: continuity of the spline (must be degree-1!) |
| | `..%f_base%modes`        | INTEGER     | 1                                 | Fourier-base: Total number of modes |
| | `..%f_base%sin_cos`      | INTEGER     | 1                                 | Fourier-base: which real modes <br> 1: only `sin(m*theta-n*nfp*zeta)`, 2: `cos(m*theta-n*nfp*zeta)`,3: sine and cosine |
| | `..%f_base%excl_mn_zero` | INTEGER     | 1                                 | Fourier-base: if cosine mode `m=n=0` is <br> =0: not excluded =1: excluded |
| | `..%f_base%mn`           | 2D-ARRAY    | `2 x f_base%modes`                | Fourier-base: Corresponding m,n-mode number for rows in `..%coef` |
| | `..%f_base%mn_max`       | 1D-ARRAY    | 2                                 | Fourier-base: Maximum (m-mode) and (n-mode // `nfp`) number in `.dat` |
| | `..%f_base%modes_sin`    | INTEGER     | 1                                 | Fourier-base: Number of sine modes   |
| | `..%f_base%modes_cos`    | INTEGER     | 1                                 | Fourier-base: Number of cosine modes |
| | `..%f_base%range_sin`    | 1D-ARRAY    | 2                                 | Fourier-base: Rows in `..%coef` that belong to sine   |
| | `..%f_base%range_cos`    | 1D-ARRAY    | 2                                 | Fourier-base: Rows in `..%coef` that belong to cosine |
| | `..%coef`                | 2D-ARRAY    | `f_base%modes x ..%s_base%nbase"` | Fourier-base: Spline coefficients for each Fourier mode |
|**>**| **Profiles, interpolated values at GREVILLE points in s (can be used to initialize a spline of the same basis as X1%s):**   ||||
| | `profile%greville%nPoints` | INTEGER     | 1                                 | Number of elements in each profile array |
| | `profile%greville%spos`    | 1D-ARRAY    | `profile%greville%nPoints`        | Grevielle points |
| | `profile%greville%phi`     | 1D-ARRAY    | `profile%greville%nPoints`        | Toroidal profile |
| | `profile%greville%chi`     | 1D-ARRAY    | `profile%greville%nPoints`        | Poloidal profile |
| | `profile%greville%iota`    | 1D-ARRAY    | `profile%greville%nPoints`        | Iota profile     |
| | `profile%greville%pres`    | 1D-ARRAY    | `profile%greville%nPoints`        | Pressure profile |
| | `profile%greville%dphi`    | 1D-ARRAY    | `profile%greville%nPoints`        | Derivative of toroidal profile w.r.t 'radial' direction s |
| | `profile%greville%dchi`    | 1D-ARRAY    | `profile%greville%nPoints`        | Derivative of poloidal profile w.r.t 'radial' direction s |
|**>**| **Profiles, coefficients (control points) of spline (can be used to initialize a spline of the same basis as X1%s):**   ||||
| | `profile%coef%nPoints`     | INTEGER     | 1                                 | Number of elements in each profile array |
| | `profile%coef%phi`         | 1D-ARRAY    | `profile%coef%nPoints`            | Toroidal profile |
| | `profile%coef%chi`         | 1D-ARRAY    | `profile%coef%nPoints`            | Poloidal profile |
| | `profile%coef%iota`        | 1D-ARRAY    | `profile%coef%nPoints`            | Iota profile     |
| | `profile%coef%pres`        | 1D-ARRAY    | `profile%coef%nPoints`            | Pressure profile |
| | `profile%coef%dphi`        | 1D-ARRAY    | `profile%coef%nPoints`            | Derivative of toroidal profile w.r.t 'radial' direction s |
| | `profile%coef%dchi`        | 1D-ARRAY    | `profile%coef%nPoints`            | Derivative of poloidal profile w.r.t 'radial' direction s |
|**>**| **Disabled**         ||||
| | `a_minor`                | DOUBLE      | 1                                 |  |
| | `r_major`                | DOUBLE      | 1                                 |  |
| | `volume`                 | DOUBLE      | 1                                 |  |

[^FN-spline]: *Non-uniform B-Splines, only having maximum continuity `degree-1`*