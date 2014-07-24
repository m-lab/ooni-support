# mlab-ns-simulator #

## Quickstart ##

### Dependencies ###

You must have a non-empty `virtualenv` folder in the `ooni-support` directory.
If you initially did a `git clone --recursive` on it should already be there.
Otherwise you should be able to do `git submodule init && git submodule
update` to correctly populate this directory.

### unit tests ###

Run `./setup.py test`.  This installs test-related tools and dependencies
under `./build/test/venv`.  Other test-related stuff goes into `./build/test`.
For example, `./build/test/htmlcov/index.html` is the test coverage report.
Hack away!

### running the server ###

This is a quick and relatively clean way:

1. `./setup.py test`
1. `./build/test/venv/bin/mlabsim --log-level DEBUG`

This will run the "quarantined" virtualenv installation which will have
the right dependencies and won't interfere with your base python system.
The server doesn't read or write any local files, so there's no need to
worry about that kind of state.

### server interaction ###

The server is basically a very simple JSON put/get thing.  The only stipulation
is that the JSON contain an `fqdn` key.  Of course, to emulate the real
`mlab-ns` or to be useful to Ooni there may need to be other fields.

#### Putting JSON with curl ####

    $ curl -sv --request PUT --data-binary '@-' 'http://127.0.0.1:8585/update-ooni'
    {
      "city": "Mountain View",
      "country": "US",
      "fqdn": "npad.iupui.mlab3.nuq02.measurement-lab.org",
      "ip": [
        "149.20.5.102",
        "2001:4F8:1:1001::102"
      ],
      "port": "8001",
      "site": "nuq02",
      "url": "http://npad.iupui.mlab3.nuq02.measurement-lab.org:8000",
      "tool_extra": {"favorite fruit": "persimmon"}
    }
    ^D

Note: I like the `-sv` options to show HTTP headers, but they are not
necessary.

Note: The port 8585 is hard coded into the python.

#### Fetching all JSON entries with curl ####

    $ curl -sv 'http://127.0.0.1:8585/ooni?match=all'

Note: This is supposed to look like production `mlab-ns` except it *requires*
`match=all` (which doesn't exist in production), and it optionally allows
`format=json` but no other `format` value, and it ignores all other parameters.
