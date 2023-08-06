# {py:mod}`itkwasm.polydata`

```{py:module} itkwasm.polydata
```

```{autodoc2-docstring} itkwasm.polydata
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`PolyDataType <itkwasm.polydata.PolyDataType>`
  - ```{autodoc2-docstring} itkwasm.polydata.PolyDataType
    :summary:
    ```
* - {py:obj}`PolyData <itkwasm.polydata.PolyData>`
  - ```{autodoc2-docstring} itkwasm.polydata.PolyData
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_default_points <itkwasm.polydata._default_points>`
  - ```{autodoc2-docstring} itkwasm.polydata._default_points
    :summary:
    ```
````

### API

`````{py:class} PolyDataType
:canonical: itkwasm.polydata.PolyDataType

```{autodoc2-docstring} itkwasm.polydata.PolyDataType
```

````{py:attribute} pointPixelComponentType
:canonical: itkwasm.polydata.PolyDataType.pointPixelComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.pointPixelComponentType
```

````

````{py:attribute} pointPixelType
:canonical: itkwasm.polydata.PolyDataType.pointPixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.pointPixelType
```

````

````{py:attribute} pointPixelComponents
:canonical: itkwasm.polydata.PolyDataType.pointPixelComponents
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.pointPixelComponents
```

````

````{py:attribute} cellPixelComponentType
:canonical: itkwasm.polydata.PolyDataType.cellPixelComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.cellPixelComponentType
```

````

````{py:attribute} cellPixelType
:canonical: itkwasm.polydata.PolyDataType.cellPixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.cellPixelType
```

````

````{py:attribute} cellPixelComponents
:canonical: itkwasm.polydata.PolyDataType.cellPixelComponents
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.polydata.PolyDataType.cellPixelComponents
```

````

`````

````{py:function} _default_points() -> numpy.typing.ArrayLike
:canonical: itkwasm.polydata._default_points

```{autodoc2-docstring} itkwasm.polydata._default_points
```
````

`````{py:class} PolyData
:canonical: itkwasm.polydata.PolyData

```{autodoc2-docstring} itkwasm.polydata.PolyData
```

````{py:attribute} polyDataType
:canonical: itkwasm.polydata.PolyData.polyDataType
:type: typing.Union[itkwasm.polydata.PolyDataType, typing.Dict]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.polyDataType
```

````

````{py:attribute} name
:canonical: itkwasm.polydata.PolyData.name
:type: str
:value: >
   'PolyData'

```{autodoc2-docstring} itkwasm.polydata.PolyData.name
```

````

````{py:attribute} numberOfPoints
:canonical: itkwasm.polydata.PolyData.numberOfPoints
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.numberOfPoints
```

````

````{py:attribute} points
:canonical: itkwasm.polydata.PolyData.points
:type: numpy.typing.ArrayLike
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.points
```

````

````{py:attribute} verticesBufferSize
:canonical: itkwasm.polydata.PolyData.verticesBufferSize
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.verticesBufferSize
```

````

````{py:attribute} vertices
:canonical: itkwasm.polydata.PolyData.vertices
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.vertices
```

````

````{py:attribute} linesBufferSize
:canonical: itkwasm.polydata.PolyData.linesBufferSize
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.linesBufferSize
```

````

````{py:attribute} lines
:canonical: itkwasm.polydata.PolyData.lines
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.lines
```

````

````{py:attribute} polygonsBufferSize
:canonical: itkwasm.polydata.PolyData.polygonsBufferSize
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.polygonsBufferSize
```

````

````{py:attribute} polygons
:canonical: itkwasm.polydata.PolyData.polygons
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.polygons
```

````

````{py:attribute} triangleStripsBufferSize
:canonical: itkwasm.polydata.PolyData.triangleStripsBufferSize
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.triangleStripsBufferSize
```

````

````{py:attribute} triangleStrips
:canonical: itkwasm.polydata.PolyData.triangleStrips
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.triangleStrips
```

````

````{py:attribute} numberOfPointPixels
:canonical: itkwasm.polydata.PolyData.numberOfPointPixels
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.numberOfPointPixels
```

````

````{py:attribute} pointData
:canonical: itkwasm.polydata.PolyData.pointData
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.pointData
```

````

````{py:attribute} numberOfCellPixels
:canonical: itkwasm.polydata.PolyData.numberOfCellPixels
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.polydata.PolyData.numberOfCellPixels
```

````

````{py:attribute} cellData
:canonical: itkwasm.polydata.PolyData.cellData
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.polydata.PolyData.cellData
```

````

````{py:method} __post_init__()
:canonical: itkwasm.polydata.PolyData.__post_init__

```{autodoc2-docstring} itkwasm.polydata.PolyData.__post_init__
```

````

`````
