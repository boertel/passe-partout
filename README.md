# passe-partout

Passe-partout is a Lazy Decentralized Locking Mechanism.

## Usage
when working on http://github.com/owner/repo, three actions are supported: ```lock```, ```unlock``` and ```status```

```
$ passepartout lock owner/repo "Reason why I lock the deployment for this service"
locked
```

```
$ passepartout unlock owner/repo
unlocked
```

```
$ passepartout status owner/repo
unlocked
```

## How it works
The command is adding (```lock```) or removing (```unlock```) a ```.lock``` file at the root of your repo. It **DOES NOT ENFORCE** the deployment of the service, it's the responsibality of the deployment tool to able the presence (or inexistance) of ```.lock```

If relying on ```git push``` to deploy your service, this ```pre-push``` git hook would not allow you to push in case the service is locked:
```
#!/bin/bash

LOCK_FILE=$(git rev-parse --show-toplevel)/.lock
if [[ -f $LOCK_FILE ]]; then
    echo "deployment is locked"
    echo "reason: $(cat $LOCK_FILE)"
    exit 1
fi
```
Note: ```git root``` com


## Etymology

*Passe-partout* is a fictional character from the game TV show [Fort Boyard](https://en.wikipedia.org/wiki/Fort_Boyard_(TV_series)). His role is to keep keys collected by the players during multiples challenges.
