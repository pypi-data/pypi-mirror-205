# {py:mod}`itkwasm.pointset`

```{py:module} itkwasm.pointset
```

```{autodoc2-docstring} itkwasm.pointset
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`PointSetType <itkwasm.pointset.PointSetType>`
  - ```{autodoc2-docstring} itkwasm.pointset.PointSetType
    :summary:
    ```
* - {py:obj}`PointSet <itkwasm.pointset.PointSet>`
  - ```{autodoc2-docstring} itkwasm.pointset.PointSet
    :summary:
    ```
````

### API

`````{py:class} PointSetType
:canonical: itkwasm.pointset.PointSetType

```{autodoc2-docstring} itkwasm.pointset.PointSetType
```

````{py:attribute} dimension
:canonical: itkwasm.pointset.PointSetType.dimension
:type: int
:value: >
   3

```{autodoc2-docstring} itkwasm.pointset.PointSetType.dimension
```

````

````{py:attribute} pointComponentType
:canonical: itkwasm.pointset.PointSetType.pointComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSetType.pointComponentType
```

````

````{py:attribute} pointPixelComponentType
:canonical: itkwasm.pointset.PointSetType.pointPixelComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSetType.pointPixelComponentType
```

````

````{py:attribute} pointPixelType
:canonical: itkwasm.pointset.PointSetType.pointPixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSetType.pointPixelType
```

````

````{py:attribute} pointPixelComponents
:canonical: itkwasm.pointset.PointSetType.pointPixelComponents
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.pointset.PointSetType.pointPixelComponents
```

````

`````

`````{py:class} PointSet
:canonical: itkwasm.pointset.PointSet

```{autodoc2-docstring} itkwasm.pointset.PointSet
```

````{py:attribute} pointSetType
:canonical: itkwasm.pointset.PointSet.pointSetType
:type: typing.Union[itkwasm.pointset.PointSetType, typing.Dict]
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSet.pointSetType
```

````

````{py:attribute} name
:canonical: itkwasm.pointset.PointSet.name
:type: str
:value: >
   'PointSet'

```{autodoc2-docstring} itkwasm.pointset.PointSet.name
```

````

````{py:attribute} numberOfPoints
:canonical: itkwasm.pointset.PointSet.numberOfPoints
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.pointset.PointSet.numberOfPoints
```

````

````{py:attribute} points
:canonical: itkwasm.pointset.PointSet.points
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSet.points
```

````

````{py:attribute} numberOfPointPixels
:canonical: itkwasm.pointset.PointSet.numberOfPointPixels
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.pointset.PointSet.numberOfPointPixels
```

````

````{py:attribute} pointData
:canonical: itkwasm.pointset.PointSet.pointData
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.pointset.PointSet.pointData
```

````

````{py:method} __post_init__()
:canonical: itkwasm.pointset.PointSet.__post_init__

```{autodoc2-docstring} itkwasm.pointset.PointSet.__post_init__
```

````

`````
