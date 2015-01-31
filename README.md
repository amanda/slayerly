# slayerly
the most metal url shortener not on the web.

## usage:
first:
```pip install -r requirements.txt```

then initialize the database in the python interpreter:
```
import slayerly
slayerly.init_db()
```
this creates a "slayer.db" sqlite3 database in your local directory.

finally, run:
```python slayerly.py```

and head to localhost:5000 in your favorite browser to get your new link \m/

## todo
- make links go to localhost:5000/slayerlyric instead of localhost:5000/id
- check for dupe urls
