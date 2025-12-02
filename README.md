# The missing feature in TONEX Editor

If you don't know anything about TONEX Pedal, then refer to IK Multimedia.
It's for guitarists.
If you're not, then learn to play guitar!

## What missing feature?

TONEX Editor is a very powerful tool, but it has one small drawback: every time you move a preset from your TONEX Pedal to the library, it creates a duplicate, renamed PresetName_01, then _02, and so on.
By the end, you’re completely lost.

So, I wrote this little piece of Python code to solve my three needs:

- Simple: delete a preset
- Almost simple: rename a preset (yes, you can do this in TONEX Editor too, but this way it’s much faster)
- Bold: remove all the _01, _02, etc. In fact, it does the job even better...

## In detail
Suppose you have a preset named PresetName, and three duplicates: PresetName_01, PresetName_02, PresetName_03.
The cleanup function will do this:

- PresetName → deleted
- PresetName_01 → deleted
- PresetName_02 → deleted
- PresetName_03 → renamed to PresetName

This way, you keep only the latest version of the preset.

# Install and use

You must have python3 installed on your computer.

Download the 3 python files `tonex_actions.py`, `TONEX_Cleaner.py`, `tonex_gui.py`.

Then with the command line tool (either Terminal or PowerShell), cd to the TONEX library directory, and from here launch the TONEX_Cleaner app: `python3 \[path_to_the_python_code\]/TONEX_Cleaner.py`
And enjoy.

# Warning

Save your library first, this code is not sure and has not been validated by IK Multimedia.

Also close TONEX Editor, TONEX, etc.

Use this code at your own risk.
