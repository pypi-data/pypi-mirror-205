def compile_gvec_to_python():
    
    import subprocess
    import os
    import gvec_to_python

    libpath = gvec_to_python.__path__[0]
    
    print('\nCompiling gvec-to-python kernels ...')
    subprocess.run(['make', 
                    '-f', 
                    os.path.join(libpath, 'Makefile'),
                    'install_path=' + libpath,
                    ], check=True, cwd=libpath)
    print('Done.')

