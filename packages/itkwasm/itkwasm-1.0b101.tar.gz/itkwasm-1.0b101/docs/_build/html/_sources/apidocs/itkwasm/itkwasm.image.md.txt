# {py:mod}`itkwasm.image`

```{py:module} itkwasm.image
```

```{autodoc2-docstring} itkwasm.image
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ImageType <itkwasm.image.ImageType>`
  - ```{autodoc2-docstring} itkwasm.image.ImageType
    :summary:
    ```
* - {py:obj}`Image <itkwasm.image.Image>`
  - ```{autodoc2-docstring} itkwasm.image.Image
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_default_direction <itkwasm.image._default_direction>`
  - ```{autodoc2-docstring} itkwasm.image._default_direction
    :summary:
    ```
````

### API

`````{py:class} ImageType
:canonical: itkwasm.image.ImageType

```{autodoc2-docstring} itkwasm.image.ImageType
```

````{py:attribute} dimension
:canonical: itkwasm.image.ImageType.dimension
:type: int
:value: >
   2

```{autodoc2-docstring} itkwasm.image.ImageType.dimension
```

````

````{py:attribute} componentType
:canonical: itkwasm.image.ImageType.componentType
:type: typing.Union[itkwasm.int_types.IntTypes, itkwasm.float_types.FloatTypes]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.ImageType.componentType
```

````

````{py:attribute} pixelType
:canonical: itkwasm.image.ImageType.pixelType
:type: itkwasm.pixel_types.PixelTypes
:value: >
   None

```{autodoc2-docstring} itkwasm.image.ImageType.pixelType
```

````

````{py:attribute} components
:canonical: itkwasm.image.ImageType.components
:type: int
:value: >
   1

```{autodoc2-docstring} itkwasm.image.ImageType.components
```

````

`````

````{py:function} _default_direction() -> numpy.typing.ArrayLike
:canonical: itkwasm.image._default_direction

```{autodoc2-docstring} itkwasm.image._default_direction
```
````

`````{py:class} Image
:canonical: itkwasm.image.Image

```{autodoc2-docstring} itkwasm.image.Image
```

````{py:attribute} imageType
:canonical: itkwasm.image.Image.imageType
:type: typing.Union[itkwasm.image.ImageType, typing.Dict]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.imageType
```

````

````{py:attribute} name
:canonical: itkwasm.image.Image.name
:type: str
:value: >
   'Image'

```{autodoc2-docstring} itkwasm.image.Image.name
```

````

````{py:attribute} origin
:canonical: itkwasm.image.Image.origin
:type: typing.Sequence[float]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.origin
```

````

````{py:attribute} spacing
:canonical: itkwasm.image.Image.spacing
:type: typing.Sequence[float]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.spacing
```

````

````{py:attribute} direction
:canonical: itkwasm.image.Image.direction
:type: numpy.typing.ArrayLike
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.direction
```

````

````{py:attribute} size
:canonical: itkwasm.image.Image.size
:type: typing.Sequence[int]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.size
```

````

````{py:attribute} metadata
:canonical: itkwasm.image.Image.metadata
:type: typing.Dict
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.metadata
```

````

````{py:attribute} data
:canonical: itkwasm.image.Image.data
:type: typing.Optional[numpy.typing.ArrayLike]
:value: >
   None

```{autodoc2-docstring} itkwasm.image.Image.data
```

````

````{py:method} __post_init__()
:canonical: itkwasm.image.Image.__post_init__

```{autodoc2-docstring} itkwasm.image.Image.__post_init__
```

````

`````
