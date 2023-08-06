# {py:mod}`itkwasm.pipeline`

```{py:module} itkwasm.pipeline
```

```{autodoc2-docstring} itkwasm.pipeline
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Pipeline <itkwasm.pipeline.Pipeline>`
  - ```{autodoc2-docstring} itkwasm.pipeline.Pipeline
    :summary:
    ```
````

### API

`````{py:class} Pipeline(pipeline: typing.Union[str, pathlib.Path, bytes])
:canonical: itkwasm.pipeline.Pipeline

```{autodoc2-docstring} itkwasm.pipeline.Pipeline
```

```{rubric} Initialization
```

```{autodoc2-docstring} itkwasm.pipeline.Pipeline.__init__
```

````{py:method} run(args: typing.List[str], outputs: typing.List[itkwasm.pipeline_output.PipelineOutput] = [], inputs: typing.List[itkwasm.pipeline_input.PipelineInput] = []) -> typing.Tuple[itkwasm.pipeline_output.PipelineOutput]
:canonical: itkwasm.pipeline.Pipeline.run

```{autodoc2-docstring} itkwasm.pipeline.Pipeline.run
```

````

````{py:method} _wasmtime_lift(ptr: int, size: int)
:canonical: itkwasm.pipeline.Pipeline._wasmtime_lift

```{autodoc2-docstring} itkwasm.pipeline.Pipeline._wasmtime_lift
```

````

````{py:method} _wasmtime_lower(ptr: int, data: typing.Union[bytes, bytearray])
:canonical: itkwasm.pipeline.Pipeline._wasmtime_lower

```{autodoc2-docstring} itkwasm.pipeline.Pipeline._wasmtime_lower
```

````

````{py:method} _set_input_array(data_array: typing.Union[bytes, bytearray], input_index: int, sub_index: int) -> int
:canonical: itkwasm.pipeline.Pipeline._set_input_array

```{autodoc2-docstring} itkwasm.pipeline.Pipeline._set_input_array
```

````

````{py:method} _set_input_json(data_object: typing.Dict, input_index: int) -> None
:canonical: itkwasm.pipeline.Pipeline._set_input_json

```{autodoc2-docstring} itkwasm.pipeline.Pipeline._set_input_json
```

````

````{py:method} _get_output_json(output_index: int) -> typing.Dict
:canonical: itkwasm.pipeline.Pipeline._get_output_json

```{autodoc2-docstring} itkwasm.pipeline.Pipeline._get_output_json
```

````

`````
