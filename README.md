# python-pocket-cli

## Installation

```bash
git clone https://github.com/kumarstack55/python-pocket-cli
cd python-pocket-cli

poetry install
poetry shell

export POCKET_CONSUMER_KEY='x'
export POCKET_ACCESS_TOKEN='x'

./pocket-cli.py -h
./pocket_cli.py retrieve -h
./pocket_cli.py add -h

./pocket_cli.py add --url http://www.example.com/
```

## See also

* https://github.com/rakanalh/pocket-api
* http://reader.fxneumann.de/plugins/oneclickpocket/auth.php
* https://github.com/tapanpandita/pocket
