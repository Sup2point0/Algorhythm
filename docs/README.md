# Algorhythm Docs

For whoever it may prove useful for, this project includes a little documentation.


<br>


## Index

| file | purpose |
| :--- | :------ |
| [Internals](intern.md) | Overview of the project, technical details, lessons learnt. |
| [Charting](charting.md) | How to create charts for the game. |
| [Dev Notes](dev.md) | Notes for myself during development. |
| [Ideas](ideas.md) | Ideas for future features. |

<!-- I love my tables, don’t I -->


<br>


## Syntax

I have a slightly unconventional Python syntax style, which I explain [here](https://github.com/Sup2point0/Assort/blob/origin/~writing/Python%20Syntax.md).

### Docstrings
Most functions include a table in their docstring outlining what arguments they take. It’s not especially pretty in code, but Visual Studio Code will show an object’s docstring when it is hovered over, and has the incredibly useful feature of being able to render Markdown in that popup – giving us a nice orderly table.

```py
| parameter | type | notes |
| `name` | `class` | description |
```

The `parameter` column lists the names of the parameters, in the preferred order for specifying them (sometimes order is messed up by some not having default values). This used to be called `argument`, but it turns out there’s a subtle difference between ‘parameter’ and ‘argument’.[^1]

[^1]: https://stackoverflow.com/questions/156767/whats-the-difference-between-an-argument-and-a-parameter
