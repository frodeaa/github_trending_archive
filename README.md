# GitHub Trending Archive

Archive of the GitHub daily trending git repositories

The repository follows:

 - [go](https://github.com/trending?l=go)
 - [java](https://github.com/trending?l=java)
 - [javascript](https://github.com/trending?l=javascript)
 - [python](https://github.com/trending?l=python)

## Install

Add ``bin/archive-trending`` to your crontab.

    crontab -l | { cat; echo "0 0 * * * $(pwd)/archive-trending"; } | crontab -