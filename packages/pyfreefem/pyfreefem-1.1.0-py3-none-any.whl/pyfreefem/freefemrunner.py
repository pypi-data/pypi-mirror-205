# This file is part []reeFEM.
#
# PyFreeFEM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# PyFreeFEM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.
from os import path
from .preprocessor import Preprocessor
import os.path
import shutil
from .io import display, exec2, ExecException, readFFMatrix, readFFArray,   \
                   writeFFArray, writeFFMatrix 
import tempfile
import numpy as np
import scipy.sparse as sp
import pymedit



class FreeFemRunner:
    """A class to run a FreeFem code given by an interpreter or raw code."""
    
    def __init__(self, code, config=dict(), run_dir=None,
                 run_file=None, debug=0, plot=False, 
                 macro_files=[]):
        """
        Usage
        _____
        Load a single file .edp file
        >>> runner=FreeFemRunner('solveState.edp')

        Load a list of files (to be assembled consecutively)
        >>> runner=FreeFemRunner(['params.edp','solveState.edp'])

        Load a single file with an updated configuration
        >>> runner=FreeFemRunner('solveState.edp',{'ITER':'0010'})

        Load raw code
        >>> code = "mesh Th=square(10,10);"
            runner=FreeFemRunner(code)

        Load a pyfreefem.Preprocessor object
        >>> preproc = Preprocessor('solveState.edp')
            runner = FreeFemRunner(preproc)

        Then execute the code with `~FreeFemRunner.execute':
        >>> runner.execute();
            runner.execute({'Re':30}); # Update magic variable value

        It is possible to execute the code in parallel with ff-mpirun by using
        >>> # Run on 4 cpus with ff-mpirun -np 4
            runner.execute(ncpu=4); 
        >>> # Run on 1 cpu with ff-mpirun -np 1
            runner.execute(ncpu=1,with_mpi=1);

        Note that in that case, a magic variable 'WITH_MPI' is automatically
        assigned and set to 1, which is useful to make adaptations in the 
        source code, e.g. 
        ```
        IF WITH_MPI
        /* Instructions to do if the code is parallel */
        ELSE
        /* Instructions to do if the code is not parallel */
        int mpirank = 0; 
        int mpisize = 1;
        ENDIF
        ```

        Parameters 
        ----------

        :param code:    raw text code, instance of Preprocessor, or files

        :param config:  a default assignment of magic variables
                        which can be modified later on during the execute() 
                        operation.

        :param run_dir: where the running script will be written. If this 
                        argument is speficied, then run_dir is not 
                        deleted after the FreeFEM execution.

        :param run_file: name of the written script

        :param debug:   tuning for verbosity. The FreeFEM command is 
                        is displayed if debug>=1.
                        Details of the parsing operation are displayed if 
                        debug>=10.

        :param plot: (default False). If set to True, then FreeFEM is run
                        with the graphical -wg option.

        :param macro_files: list of enhanced .edp dependency files
                        (with meta-instructions)
                        which are also to be parsed and placed in the 
                        run folder of the final executable.

        :param verbosity:     : verbosity level of FreeFem output

        Executing the code creates (by default) a temporary file which is
        to be executed by FreeFEM and which is removed after the python 
        execution. This behavior can be changed by using the
        `run_dir` and `run_file` arguments. 

        Note : for some usage, it is necessary to modify the
               FreeFem command. This can be achieved by
               updating the method `~FreeFemRunner.cmd`
               See pyfreefem/examples/hello_world_vglrun.py 

        """
        self.freefemFiles = dict()
        self.debug = int(debug)
        self.plot = plot
        self.run_file = run_file
        self.run_time = -1
        self.exports = []

        #: pyfreefem standard output.   
        #: After calling :py:meth:`pyfreefem.FreeFemRunner.execute` 
        #: py:attr:`pyfreefem.FreeFemRunner.rets` is a tuple    
        #: containing:  
        #:  
        #: * rets[0]: the return code   
        #: * rets[1]: stdout    
        #: * rets[2]: stderr    
        #: * rets[3]: the whole standard output
        self.rets = tuple() 

        # create temporary directory if needed
        self.__context__ = False

        if run_dir is None:
            self.tempdir = tempfile.TemporaryDirectory(prefix="pyfreefem_")
            self.run_dir = self.tempdir.name
        else:   
            self.run_dir = str(run_dir)

        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)
            display("Create "+self.run_dir, level=10, debug=self.debug,
                    color="magenta")
        self.ffexport_dir = self.run_dir+'/ffexport'
        self.ffimport_dir = self.run_dir+'/ffimport'

        if isinstance(code, Preprocessor):
            self.preprocessor = code
        else:
            self.preprocessor = Preprocessor(code, config, debug=self.debug-10)
        self.config = config


        if self.run_file is None:
            if isinstance(code,list) and os.path.isfile(code[0]):
                self.run_file = os.path.basename(code[0])
            elif os.path.isfile(code):
                self.run_file = os.path.basename(code)
            else:
                self.run_file = "run.edp"

        self.macro_files = macro_files
        #self.macro_files.append(os.path.dirname(__file__)+"/edp/io.edp")
        
    def import_variables(self, **kwargs):
        # Clean the ffexport_dir 
        if os.path.exists(self.ffimport_dir):
            shutil.rmtree(self.ffimport_dir, ignore_errors=True)
        os.makedirs(self.ffimport_dir)
        display("Reset directory "+self.ffimport_dir, level=10, debug=self.debug, 
                color="magenta")
        # Import python variables to FreeFEM
        for varname, var in kwargs.items():
            if isinstance(var,float):   
                with open(self.ffimport_dir+"/var_"+varname,"w") as f:  
                    f.write(str(var)+"\n")
            elif isinstance(var,np.ndarray) and len(var.shape)==1:        
                writeFFArray(var, self.ffimport_dir+"/array_"+varname)
            elif isinstance(var,np.ndarray) or sp.issparse(var):    
                writeFFMatrix(var, self.ffimport_dir+"/matrix_"+varname)
            elif isinstance(var,pymedit.mesh.Mesh):
                var.save(self.ffimport_dir+"/mesh_"+varname+".mesh")
            elif isinstance(var,pymedit.mesh3D.Mesh3D):
                var.save(self.ffimport_dir+"/mesh3D_"+varname+".mesh")
            else:   
                raise Exception("Error, type "+str(type(var)) + " is unknown for pyfreefem import." 
                                " Supported types are float, np.ndarray, pymedit.mesh.Mesh and "    
                                "pymedit.mesh3D.Mesh3D.")

    def parse(self, config):    
        """ Parse"""
        return self.preprocessor.parse(config)

    def write_edp_file(self, config=dict(), **kwargs):
        """
        Write the parsed .edp file in the running directory.

        Arguments
        ---------

            config      : a dictionary of magic variable which updates the 
                          default FreeFemRunner.config assignment.

            ncpu        : the number of CPUs for a run with ff-mpirun

            with_mpi    :  will run with ff-mpirun even if ncpu=1

            target_file : file name of the output .edp file to be written
        """
        ncpu = int(kwargs.get('ncpu', 1))
        self.config.update(config)
        if ncpu > 1 or kwargs.get('with_mpi', False):
            config.update({'WITH_MPI': 1})
        else:
            config.update({'WITH_MPI': 0})

        target_file = path.join(self.run_dir, self.run_file)

        self.config.update({'RUNDIR':self.run_dir})
        self.config.update({'FFEXPORTDIR':self.ffexport_dir})
        self.config.update({'FFIMPORTDIR':self.ffimport_dir})
        code = self.parse(config)
        
        f = open(target_file, "w")
        f.write(code)
        f.close()
        display("Write "+target_file, level=10, debug=self.debug,
                color="magenta")

        if self.preprocessor.imports:
            self.macro_files += self.preprocessor.imports

        if self.macro_files:
            for mf in self.macro_files:
                file_name = os.path.split(mf)[1]
                with open(self.run_dir+"/"+file_name, "w") as f:
                    f.write(Preprocessor(mf, self.config, debug=self.debug-10).parse(config))
        return target_file

    def __enter__(self):
        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)
            display("Create "+self.run_dir, level=10, debug=self.debug,
                    color="magenta")
        return self

    def __exit__(self, type, value, traceback):
        pass
            

    def execute(self, config=dict(), **kwargs):
        """
        Parse with the input config, save the code in .edp file
        and call FreeFEM.

        Usage:
            >>> runner = FreeFemRunner('solveState.edp')
            runner.execute();
            runner.execute({"ITER" : "0024"});

        Options
        -------
        config    :  dictionary of updated magic variable values
                     Warning : a "SET" instruction in the .edp file
                     always has the precedence over the values specified
                     by `config`

        debug       :  execute the edp file with an updated level of verbosity

        target_file : change of location to write the .edp file.

        silent      : (default False) if set to True, there will be no standard 
                      output displayed in the shell (although it will still be 
                      returned in the output variables stdout, stderr and mix).

        Returns
        -------

        returncode   :  the return code of the FreeFEM process
        stdout       :  the standard output
        stderr       :  the standard error output
        mix          :  the integrality of the of the FreeFEM process output 

        """
        debug = kwargs.pop('debug', self.debug)
        config.update({'DEBUG':debug})
        target_file = self.write_edp_file(config, **kwargs)
        verbosity = kwargs.get('verbosity',-1)
        silent = verbosity < 0
        if silent:
            verbosity = 0
        kwargs.update(verbosity=verbosity)
        level = kwargs.pop('level',1)

        self.exports = dict()
        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)

        # Clean the ffexport_dir 
        if os.path.exists(self.ffexport_dir):
            shutil.rmtree(self.ffexport_dir, ignore_errors=True)
        os.makedirs(self.ffexport_dir)
        display("Reset directory "+self.ffexport_dir, level=10, debug=self.debug, 
                color="magenta")


        try:
            returncode, stdout, stderr, mix = \
                exec2(self.cmd(target_file, **kwargs),
                       debug=debug, level=level, silent=silent)
        except ExecException as e:
            display(e.args[0], level = 0, debug = 0)
            display('\n'.join(e.mix.splitlines()[-40:]), level=0, debug=0)
            e.args = []
            raise e

        exportfiles = os.listdir(self.ffexport_dir)
        for file in exportfiles:
            if file.startswith('mesh_') and not file.endswith('.gmsh'):
                from pymedit import Mesh
                self.exports[file[5:-5]] = Mesh(self.ffexport_dir+"/"+file) 
            if file.startswith('mesh3D_') and not file.endswith('.gmsh'):
                from pymedit import Mesh3D
                self.exports[file[5:-5]] = Mesh3D(self.ffexport_dir+"/"+file) 
            if file.startswith('var_'): 
                with open(self.ffexport_dir+'/'+file) as f:
                    self.exports[file[4:]] = float(f.read())
            if file.startswith('array_'):
                self.exports[file[6:]] = readFFArray(self.ffexport_dir+'/'+file)
            if file.startswith('matrix_'):
                self.exports[file[7:]] = readFFMatrix(self.ffexport_dir+'/'+file)

        self.rets =(returncode, stdout, stderr, mix) #: pyfreefem standard output
        return self.exports


    def cmd(self, target_file, **kwargs):
        """Return the shell command that is to be run."""
        ncpu = kwargs.get('ncpu', 1)
        if ncpu > 1 or kwargs.get('with_mpi', False):
            cmd = f"ff-mpirun -np {ncpu}"
        else:
            cmd = "FreeFem++"
        cmd += " " + target_file
        if 'verbosity' in kwargs:
            cmd = cmd+" -v "+str(kwargs['verbosity'])
        if self.plot or kwargs.get('plot', False):
            cmd = cmd+" -wg"
        elif not kwargs.get('with_mpi', False):
            cmd += " -nw"
        return cmd
