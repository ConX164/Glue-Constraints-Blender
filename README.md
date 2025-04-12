# Glue-Constraints-Blender
This is an extremely experimental addon to blender.
Run the .py from either the addon or scripting tabs. Once run sucessfully, a new section will appear under the phyics tag of objects.

To use, first ensure that all desired objects have rigid bodies created.
Then, select all the objects you wish to join. Settings can be adjusted.
Focus on the "breaking threshold" and "breakable" as they are what you most likely want.
Once ready, press the generate constraints button. This will take several minutes when dealing with > 100 objects.
>1000 or so objects are not recomended to do at once.

A new collection of contraints will be generated if successfull. If you wish to adjust the strength and breakability of the constraints,
select them all and adjust either "breakable" or "threshold multiplier" options. The threshold multiplier multiplies the strength of all constraints by the selected amount.
<1 to weaken and >1 to strengthen. Updating should take much less time than generating new constraints.
