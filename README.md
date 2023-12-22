# Atomic Blender (CIF)
Plugin for Blender software allowing the representation of crystallographic structures stored in CIF files.
This plugin is based on the "Atomic Blender (PDB/XYZ)" plugin written by Clemens Barth, and uses the same interface for loading CIF files.

![](https://user-images.githubusercontent.com/26389071/224566624-d86b0c65-4443-4613-a555-5152c2bc26c0.png)

## How to use the plugin
1. Download the whole BlenderCIF repository, extract it and keep only the `io_mesh_atomic_cif` folder.
2. Move the `io_mesh_atomic_cif` folder in your Blender's plugins directory (e.g. `C:\Program Files\Blender Foundation\Blender 3.4\3.4\scripts\addons`).
3. This plugin uses the CIF parser of the gemmi library, so this package has to be installed for Blender's python interpreter.
   - Find the path of the Blender's python interpeter (e.g. `C:\Program Files\Blender Foundation\Blender 3.4\3.4\python\bin\python.exe`),
   - In your terminal, run `myPythonPath -m pip install gemmi` by replacing `myPythonPath` by the path of your Blender's python interpeter. The gemmi package should be installed.
4. Open Blender, and in the Edit -> Preferences window, select the Add-ons tab. Type in the searchbar "atomic blender PDB/XYZ/CIF" and check the corresponding package.
5. Use File -> Import -> CIF to import CIF files.
