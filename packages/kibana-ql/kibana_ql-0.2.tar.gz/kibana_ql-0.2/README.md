# kibana-ql

Parser for the Kibana Query Language (KQL).

## Install

```shell
pip install kibana-ql
```

## Use

```python
from kibana_ql import KqlParser
p = KqlParser()
tree = p.parse("field: value")
p.ast(tree)  # {'field': 'field', 'value': 'value'}
tree = p.parse('document: "tax" and @date > now-2w')
p.ast(tree)  # {'op': 'and', 'left': {'field': 'document', 'value': 'tax'}, 'right': {'field': '@date', 'op': '>', 'value': ('now-2w',)}}
```

## Tests

```shell
py -m unittest discover -v -s tests -p "*_test.py"
```

## Notes

Grammar file based on <https://github.com/elastic/kibana/blob/main/packages/kbn-es-query/src/kuery/grammar/grammar.peggy>.
