# {py:mod}`itkwasm.pyodide`

```{py:module} itkwasm.pyodide
```

```{autodoc2-docstring} itkwasm.pyodide
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`JsPackageConfig <itkwasm.pyodide.JsPackageConfig>`
  - ```{autodoc2-docstring} itkwasm.pyodide.JsPackageConfig
    :summary:
    ```
* - {py:obj}`JsPackage <itkwasm.pyodide.JsPackage>`
  - ```{autodoc2-docstring} itkwasm.pyodide.JsPackage
    :summary:
    ```
* - {py:obj}`JsResources <itkwasm.pyodide.JsResources>`
  - ```{autodoc2-docstring} itkwasm.pyodide.JsResources
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`to_py <itkwasm.pyodide.to_py>`
  - ```{autodoc2-docstring} itkwasm.pyodide.to_py
    :summary:
    ```
* - {py:obj}`to_js <itkwasm.pyodide.to_js>`
  - ```{autodoc2-docstring} itkwasm.pyodide.to_js
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`js_resources <itkwasm.pyodide.js_resources>`
  - ```{autodoc2-docstring} itkwasm.pyodide.js_resources
    :summary:
    ```
````

### API

`````{py:class} JsPackageConfig
:canonical: itkwasm.pyodide.JsPackageConfig

```{autodoc2-docstring} itkwasm.pyodide.JsPackageConfig
```

````{py:attribute} module_url
:canonical: itkwasm.pyodide.JsPackageConfig.module_url
:type: str
:value: >
   None

```{autodoc2-docstring} itkwasm.pyodide.JsPackageConfig.module_url
```

````

````{py:attribute} pipelines_base_url
:canonical: itkwasm.pyodide.JsPackageConfig.pipelines_base_url
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} itkwasm.pyodide.JsPackageConfig.pipelines_base_url
```

````

````{py:attribute} pipeline_worker_url
:canonical: itkwasm.pyodide.JsPackageConfig.pipeline_worker_url
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} itkwasm.pyodide.JsPackageConfig.pipeline_worker_url
```

````

`````

`````{py:class} JsPackage(config: itkwasm.pyodide.JsPackageConfig)
:canonical: itkwasm.pyodide.JsPackage

```{autodoc2-docstring} itkwasm.pyodide.JsPackage
```

```{rubric} Initialization
```

```{autodoc2-docstring} itkwasm.pyodide.JsPackage.__init__
```

````{py:property} config
:canonical: itkwasm.pyodide.JsPackage.config

```{autodoc2-docstring} itkwasm.pyodide.JsPackage.config
```

````

````{py:property} js_module
:canonical: itkwasm.pyodide.JsPackage.js_module

```{autodoc2-docstring} itkwasm.pyodide.JsPackage.js_module
```

````

`````

`````{py:class} JsResources()
:canonical: itkwasm.pyodide.JsResources

```{autodoc2-docstring} itkwasm.pyodide.JsResources
```

```{rubric} Initialization
```

```{autodoc2-docstring} itkwasm.pyodide.JsResources.__init__
```

````{py:property} web_worker
:canonical: itkwasm.pyodide.JsResources.web_worker

```{autodoc2-docstring} itkwasm.pyodide.JsResources.web_worker
```

````

`````

````{py:data} js_resources
:canonical: itkwasm.pyodide.js_resources
:value: >
   None

```{autodoc2-docstring} itkwasm.pyodide.js_resources
```

````

````{py:function} to_py(js_proxy)
:canonical: itkwasm.pyodide.to_py

```{autodoc2-docstring} itkwasm.pyodide.to_py
```
````

````{py:function} to_js(py)
:canonical: itkwasm.pyodide.to_js

```{autodoc2-docstring} itkwasm.pyodide.to_js
```
````
