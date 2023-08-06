# {py:mod}`itkwasm.environment_dispatch`

```{py:module} itkwasm.environment_dispatch
```

```{autodoc2-docstring} itkwasm.environment_dispatch
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FunctionFactory <itkwasm.environment_dispatch.FunctionFactory>`
  - ```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`environment_dispatch <itkwasm.environment_dispatch.environment_dispatch>`
  - ```{autodoc2-docstring} itkwasm.environment_dispatch.environment_dispatch
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`function_factory <itkwasm.environment_dispatch.function_factory>`
  - ```{autodoc2-docstring} itkwasm.environment_dispatch.function_factory
    :summary:
    ```
````

### API

`````{py:class} FunctionFactory()
:canonical: itkwasm.environment_dispatch.FunctionFactory

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory
```

```{rubric} Initialization
```

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.__init__
```

````{py:method} register(interface_package: str, func_name: str, func: typing.Callable, priority: int = 1) -> None
:canonical: itkwasm.environment_dispatch.FunctionFactory.register

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.register
```

````

````{py:method} lookup(interface_package: str, func_name: str) -> typing.Optional[typing.Set[typing.Callable]]
:canonical: itkwasm.environment_dispatch.FunctionFactory.lookup

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.lookup
```

````

````{py:method} highest_priority(interface_package: str, func_name: str) -> typing.Optional[typing.Callable]
:canonical: itkwasm.environment_dispatch.FunctionFactory.highest_priority

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.highest_priority
```

````

````{py:method} set_priority(func: typing.Callable, priority: int) -> None
:canonical: itkwasm.environment_dispatch.FunctionFactory.set_priority

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.set_priority
```

````

````{py:method} get_priority(func: typing.Callable) -> int
:canonical: itkwasm.environment_dispatch.FunctionFactory.get_priority

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.get_priority
```

````

````{py:method} disable(interface_package: str, func_name: str)
:canonical: itkwasm.environment_dispatch.FunctionFactory.disable

```{autodoc2-docstring} itkwasm.environment_dispatch.FunctionFactory.disable
```

````

`````

````{py:data} function_factory
:canonical: itkwasm.environment_dispatch.function_factory
:value: >
   None

```{autodoc2-docstring} itkwasm.environment_dispatch.function_factory
```

````

````{py:function} environment_dispatch(interface_package: str, func_name: str) -> typing.Callable
:canonical: itkwasm.environment_dispatch.environment_dispatch

```{autodoc2-docstring} itkwasm.environment_dispatch.environment_dispatch
```
````
