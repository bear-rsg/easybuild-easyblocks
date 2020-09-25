##
# Copyright 2009-2017 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for HEXPRESS, implemented as an easyblock.

Original author: James Birch (University of Birmingham)
Modified: Simon Branford (University of Birmingham)
"""
import os
import shutil
from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.run import run_cmd
from easybuild.tools.build_log import EasyBuildError


class EB_HEXPRESS(EasyBlock):
    """
    Support for installing HEXPRESS
    """

    def configure_step(self, cmd_prefix=''):
        """
        No configure step.
        """
        pass

    def build_step(self, verbose=False, path=None):
        """
        Run the installer - which should be patched to remove interactivity
        and to install to a local 'build' directory.
        """
        cmd = "./install_numeca"
        (out, _) = run_cmd(cmd, log_all=True, simple=False)
        return out

    def install_step(self):
        """
        Create the installation in correct location
        """
        builddir = os.path.join(self.cfg['start_dir'], 'build')
        try:
            for f in ['bin', 'COMMON', 'hexpress%s' % self.version.replace('.', ''), '_pvm']:
                src = os.path.join(builddir, f)
                target = os.path.join(self.installdir, f)
                shutil.copytree(src, target)
        except OSError as err:
            raise EasyBuildError("Failed to copy HEXPRESS files to %s: %s", target, err)
