# OpenSCAD Template

## Repository structure

This repository, as it is maintained on [GitHub](http://github.com/Feuermurmel/openscad-template), contains two important branches, Branch `master` and `examples`. `master` contains an empty project which is ready to be clones and used for new project.

Branch `examples` additionally contains a few example source files which are ready to be compiled. The root directory on that branch also contains a second text document `examples.creole`, describing the example project in more detail.


## Prerequisites

- OpenSCAD snapshot > 2014.11.05
	- Used to compile OpenSCAD source files to STL.
	- It is recommended to a recent development snapshot, e.g. version 2014.11.05 or later.
		- The current release version (2014.03) generates invalid dependency information if the path to the project contains spaces or other characters that need to be treated specially in a makefile and also has trouble with 2D shapes containing holes. The current development version solves these problems.

- Inkscape > 0.91
	- Used to export DXF files to SVG.
	- At least version 0.91 (or maybe some earlier development snapshot) is necessary because some recently added command line verbs are used to transform and massage an SVG prior to export.
	- Recommended to be used to edit SVG files, especially if its necessary to create multiple layers and import them separately in OpenSCAD.

- Python 2.7
	- Used for to run the plugin that exports DXF to SVG and to run scripts that wrap the OpenSCAD command line tool and work around problems with generation of dependency information of OpenSCAD.
	- Should already be installed as a dependency to Inkscape. The most recent version of Python 2.7 is recommended.


### Explicitly specifying paths to binaries

If any of the required binaries is not available on `$PATH` or different versions should be used, the paths to these binaries can be configured by creating a file called `config.mk` in the same directory as the makefile. There, variables can be set to the paths to these binaries (or to a different binary name which can be found on `$PATH`), like shown in the following example:

	# Path to the OpenSCAD binary
	OPENSCAD := /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD
	
	# Path to the Inkscape binary
	INKSCAPE := /opt/local/bin/inkscape
	
	# Path to the Python 2.7 binary
	PYTHON := /opt/local/bin/python2.7


## Supported file types

### SVG files

Any file whose name ends in `.svg` may be used from an OpenSCAD file like this:

	import("file.dxf");

The makefile will automatically convert the SVG file to a DXF file when building the project. If Inkscape is used to edit the SVG file, multiple layers can be created which can then be imported individually:

	import("file.dxf", "background");

The DXF export supports all shapes supported by Inkscape (e.g. rectangles, circles, paths, spiro lines, text, ...). Before the object are exported, all objects are converted to paths and combined using the union operation. Then, the resulting paths are converted to line segments which closely follow the curved parts of the path. The resulting line segments are exported to DXF and combined to the original shapes when imported in OpenSCAD. For these transformations to work, the objects need to be placed in Inkscape layers.

OpenSCAD itself does not defined in which unit any numbers are interpreted [0]. Inkscape OTOH allows the used to defined a document wide unit as well as using different units when specifying the size and position of shapes. When exporting the SVG document using Inkscape, all numbers are converted to the unit specified under ''General'' in Inkscape's ''Document Properties'' dialog. These numbers are then used when writing the DXF document and these are the numeric sizes and positions that OpenSCAD will see.

DXF and OpenSCAD both use a right-handed coordinate system (the Y axis runs up when the X-axis runs to the right). While SVG uses a left-handed coordinate system (the Y axis runs down if the same orientation is used). Inkscape, surprisingly also uses a right-handed coordinate system. The DXF export script honors that and places the origin of the document in the lower left corner when exporting the document.

[0]: Although millimeters seems to be the predominant unit.


### OpenSCAD files

Any file whose name ends in `.scad` but does not start with `_` will be compiled to STL file using OpenSCAD. OpenSCAD files whose names start with `_` can be used as "library" files and can be used from other OpenSCAD files using one of the following commands:

	include <filename>
	use <filename>

OpenSCAD files may be compiled to STL and used from other OpenSCAD files at the same time. Please see the [manual](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Print_version) for details and on how to use OpenSCAD in general.


## Generating Source files

This template includes support automatically generated source files. Currently supported for inclusion in the build process are OpenSCAD and SVG files. This works by editing the `generate_sources.sh` script.

The script defines a function `generate_file()`, which should be called in the remainder of the script once for each file which should be generated. The first argument to the function is be the name of the file to be generated, the remaining arguments a command, which when run should output the file's content to standard output. How the function `generate_file()` is called is up to the script and may e.g. be done from a `for` loop or while iterating over a set of other source files.


## Compiling

To compile the whole project, run `make` from the directory in which this readme is. This will generate all sources files, if any, process all SVG files and produce an STL file for each OpenSCAD source file whose name does not start with `_`. Individual files may be created or updated by passing their names to the make command, as usual.


### Makefile targets

These are all makefile targets which are not the path of a single file to build:

- `all`: This target will build all files that can be built from all source files. This is the default target when just running `make`.
- `clean`: Removes all built files [1].
- `generated`: Generates all files generated by `generate_sources.sh`.
- `dxf`: Converts all SVG files to DXF files.
- `stl`: Compiles all OpenSCAD files to STL files.

[1]: This will not remove files for which the source file was removed. There is no simple way to detect whether a file was previously built from a source file or was placed in the `src` directory manually.


### Settings used for compilation

The quality of the DXF export can be specified by creating a file called `settings.mk` in the same directory as the makefile. Setting `DXF_FLATNESS` to a smaller value (which defaults to `0.1`) creates a shape that more closely follows curved parts of the exported shapes.

	# Specify how far the exported approximation may deviate from the actual shape. The default is 0.1.
	DXF_FLATNESS := 0.02


### Dependency tracking

OpenSCAD has the ability to write dependency files which record all files used while producing an STL file. These dependency files can be read by `make`. This ability is used to only recompile necessary files when running make.

This same mechanism is currently not used for converting SVG files referring to other files or for the script used to generate source files. There, if other file are used in the process, the source file tracked by the makefile (the main SVG files or the files `generate_sources.sh` in case of generated sources) needs to be manually updated by running `touch` on the file before calling `make`.