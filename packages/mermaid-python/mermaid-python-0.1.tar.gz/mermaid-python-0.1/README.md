# mermaid-python

You can use this package to generate diagrams using Mermaid JS in a Jupyter notebook.

To install, run `pip install mermaid-python`.

You can generate a simple flowchart by running:

```python
from mermaid import Mermaid
Mermaid("graph TB\na-->b")
```

<br>
<img src="https://user-images.githubusercontent.com/4041805/235061275-b2de3344-00b0-4e6f-8d72-386abe211998.png" width=60>

You can also use themes:

```python
Mermaid("""%%{
    init: {
        'theme': 'base',
        'themeVariables': {
        'primaryColor': '#BB2528',
        'primaryTextColor': '#fff',
        'primaryBorderColor': '#7C0000',
        'lineColor': '#F8B229',
        'secondaryColor': '#006100',
        'tertiaryColor': '#fff'
        }
    }
    }%%
    graph LR
    A --- B
    B-->C[fa:fa-ban forbidden]
    B-->D(fa:fa-spinner);
""")
```

<br>
<img src="https://user-images.githubusercontent.com/4041805/235061286-bf7d8430-4f5a-4574-b555-abc8bf83ba66.png" width=300>
