# {py:mod}`itkwasm.mesh`

```{py:module} itkwasm.mesh
```

```{autodoc2-docstring} itkwasm.mesh
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`MeshType <itkwasm.mesh.MeshType>`
  - ```{autodoc2-docstring} itkwasm.mesh.MeshType
    :summary:
    ```
* - {py:obj}`Mesh <itkwasm.mesh.Mesh>`
  - ```{autodoc2-docstring} itkwasm.mesh.Mesh
    :summary:
    ```
````

### API

`````{py:class} MeshType
:canonical: itkwasm.mesh.MeshType

```{autodoc2-docstring} itkwasm.mesh.MeshType
```

````{py:attribute} dimension
:canonical: itkwasm.mesh.MeshType.dimension
:type: int
:value: >
   3

```{autodoc2-docstring} itkwasm.mesh.MeshType.dimension
```

````

````{py:attribute} pointComponentType
:canonical: itkwasm.mesh.MeshType.pointComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.pointComponentType
```

````

````{py:attribute} pointPixelComponentType
:canonical: itkwasm.mesh.MeshType.pointPixelComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.pointPixelComponentType
```

````

````{py:attribute} pointPixelType
:canonical: itkwasm.mesh.MeshType.pointPixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.pointPixelType
```

````

````{py:attribute} pointPixelComponents
:canonical: itkwasm.mesh.MeshType.pointPixelComponents
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.mesh.MeshType.pointPixelComponents
```

````

````{py:attribute} cellComponentType
:canonical: itkwasm.mesh.MeshType.cellComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.cellComponentType
```

````

````{py:attribute} cellPixelComponentType
:canonical: itkwasm.mesh.MeshType.cellPixelComponentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.cellPixelComponentType
```

````

````{py:attribute} cellPixelType
:canonical: itkwasm.mesh.MeshType.cellPixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.MeshType.cellPixelType
```

````

````{py:attribute} cellPixelComponents
:canonical: itkwasm.mesh.MeshType.cellPixelComponents
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.mesh.MeshType.cellPixelComponents
```

````

`````

`````{py:class} Mesh
:canonical: itkwasm.mesh.Mesh

```{autodoc2-docstring} itkwasm.mesh.Mesh
```

````{py:attribute} meshType
:canonical: itkwasm.mesh.Mesh.meshType
:type: typing.Union[itkwasm.mesh.MeshType, typing.Dict]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.Mesh.meshType
```

````

````{py:attribute} name
:canonical: itkwasm.mesh.Mesh.name
:type: str
:value: >
   'Mesh'

```{autodoc2-docstring} itkwasm.mesh.Mesh.name
```

````

````{py:attribute} numberOfPoints
:canonical: itkwasm.mesh.Mesh.numberOfPoints
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.mesh.Mesh.numberOfPoints
```

````

````{py:attribute} points
:canonical: itkwasm.mesh.Mesh.points
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.Mesh.points
```

````

````{py:attribute} numberOfPointPixels
:canonical: itkwasm.mesh.Mesh.numberOfPointPixels
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.mesh.Mesh.numberOfPointPixels
```

````

````{py:attribute} pointData
:canonical: itkwasm.mesh.Mesh.pointData
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.Mesh.pointData
```

````

````{py:attribute} numberOfCells
:canonical: itkwasm.mesh.Mesh.numberOfCells
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.mesh.Mesh.numberOfCells
```

````

````{py:attribute} cells
:canonical: itkwasm.mesh.Mesh.cells
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.Mesh.cells
```

````

````{py:attribute} cellBufferSize
:canonical: itkwasm.mesh.Mesh.cellBufferSize
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.mesh.Mesh.cellBufferSize
```

````

````{py:attribute} numberOfCellPixels
:canonical: itkwasm.mesh.Mesh.numberOfCellPixels
:type: int
:value: >
   0

```{autodoc2-docstring} itkwasm.mesh.Mesh.numberOfCellPixels
```

````

````{py:attribute} cellData
:canonical: itkwasm.mesh.Mesh.cellData
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.mesh.Mesh.cellData
```

````

````{py:method} __post_init__()
:canonical: itkwasm.mesh.Mesh.__post_init__

```{autodoc2-docstring} itkwasm.mesh.Mesh.__post_init__
```

````

`````
