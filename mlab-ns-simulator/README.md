mlab-ns-simulator

Quickstart

Run `./setup.py test`.  This installs test-related tools and
dependencies under `./build/test/venv`.  Other test-related stuff goes
into `./build/test`.  For example, `./build/test/htmlcov/index.html`
is the test coverage report.  Hack away!

You must have a 'virtualenv' folder in the ooni-support directory. Download the
latest version from...

https://pypi.python.org/packages/source/v/virtualenv/

...extract it, and rename the folder 'virtualenv'.

To run the server, from the mlab-ns-simulator directory, run:

    PYTHONPATH="." python2 -c 'from mlabsim import main; main.main()'
