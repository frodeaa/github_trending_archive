# GitHub Trending Archive

Archive of the GitHub daily trending git repositories

The repository follows:

 - [go](https://github.com/trending?l=go)
 - [rust](https://github.com/trending?l=rust)
 - [java](https://github.com/trending?l=java)
 - [javascript](https://github.com/trending?l=javascript)
 - [python](https://github.com/trending?l=python)

## Install

Add ``bin/archive-trending`` to your crontab.

    crontab -l | { cat; echo "0 0 * * * $(pwd)/bin/archive-trending"; } | crontab -

## Run server

Make the archive available from HTTP by running ``bin/serve``. It will be
available on http://0.0.0.0:8080. The default port can be change by
setting environment ``PORT``

    $ PORT=8000 ./bin/serve
