the data service for the touchfish app, which contains two part:
- tfdataservice: running data service (a web server)
```python
from touchfish import tfdataservice

tfdataservice.run(workpath='', port=2233)
```
- tfoperator: the python sdk for data service
```python
from touchfish import tfoperator

# init the operator
tfop = tfoperator(host='', port=2233)

# add a fish
tfop.add_fish('testtest', type='txt', description='', tags=[['test']])

# search fish
res = tfop.search_fish(tags=[['test']])
res.data
```