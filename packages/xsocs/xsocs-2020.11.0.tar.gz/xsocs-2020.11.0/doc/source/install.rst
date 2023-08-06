
Installation
============

*X-SOCS* supports `Python <https://www.python.org/>`_ versions >= 3.4 (recommended) and 2.7.

Binary wheels of the latest development version of X-SOCS are available for Linux and Windows (for python >= 3.6) in the *X-SOCS* `wheelhouse <https://kmap.gitlab-pages.esrf.fr/xsocs/wheels/>`_.

To install *X-SOCS* with minimal dependency (to use from scripts)::

    pip install --pre --find-links https://kmap.gitlab-pages.esrf.fr/xsocs/wheels/ xsocs [--user]

or with graphical user interface dependencies::

    pip install --pre --find-links https://kmap.gitlab-pages.esrf.fr/xsocs/wheels/ xsocs[gui] [--user]

.. note::
   The ``--user`` optional argument installs X-SOCS for the current user only.

Dependencies
------------

The dependencies of *X-SOCS* are:

* `Python <https://www.python.org/>`_ >=3.4 or 2.7 (Note: The Graphical user interface is only tested with python3).
* `numpy <http://www.numpy.org>`_
* `h5py <http://www.h5py.org/>`_
* `fabio <https://pypi.org/project/fabio/>`_
* `silx <https://pypi.org/project/silx>`_
* `xrayutilities <https://xrayutilities.sourceforge.io/>`_
* `scipy <https://pypi.python.org/pypi/scipy>`_
* `PyOpenGL <http://pyopengl.sourceforge.net/>`_
* `matplotlib <https://matplotlib.org/>`_
* `PyQt5 <https://riverbankcomputing.com/software/pyqt/intro>`_
* `setuptools <https://pypi.org/project/setuptools/>`_

In addition, OpenGL 2.1 is required for the 3D view of the QSpace.

Build dependencies
++++++++++++++++++

In addition to run-time dependencies, building *X-SOCS* requires:

* a C/C++ compiler
* `cython <http://cython.org/>`_ (>=0.21).

Installing from source
----------------------

Building *X-SOCS* from the source requires some `Build dependencies`_.

Building from source
++++++++++++++++++++

Clone the source `repository <https://gitlab.esrf.fr/kmap/xsocs.git>`_::

    git clone https://gitlab.esrf.fr/kmap/xsocs.git

Or download the source as a `zip file <https://gitlab.esrf.fr/kmap/xsocs/-/archive/master/xsocs-master.zip>`_ and unzip it.

Then go into the xsocs directory::

    cd xsocs

And install xsocs either with minimal dependency (to use from scripts)::

    pip install . [--user]

or with all graphical user interface dependencies::

    pip install .[gui] [--user]

