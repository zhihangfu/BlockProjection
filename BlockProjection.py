"""
Project Blocks (vertically) to selected Objects.
Currently not working with SubD
"""


import rhinoscriptsyntax as rs


# ask for inputs
blocks = rs.GetObjects(message="Select blocks to project", filter=4096, preselect=True, select=True)
targets = rs.GetObjects(message="Select surfaces, polysurfaces, SubDs and meshes to project onto", filter=8|16|32|1073741824) # not applicable for SubD(262144)

# tweak blocks one by one
count = 0
for b in blocks:
    
    if rs.IsBlockInstance(b):
        ptFrom = rs.BlockInstanceInsertPoint(b)
       
        # find pt to move to
        for t in targets:
            if rs.IsSurface(t) or rs.IsPolysurface(t):
                ptTo = rs.ProjectPointToSurface(ptFrom,t,[0,0,1])
            elif rs.IsMesh(t):
                ptTo = rs.ProjectPointToMesh(ptFrom,t,[0,0,1])
            
            if len(ptTo) != 0: break
        
        # move block vertically
        if len(ptTo) != 0:
            ptTo = ptTo[0]
            movement = rs.VectorCreate(ptTo, ptFrom)
            rs.MoveObject(b, movement)
            count += 1

# Print log to command line
print "Projected",
print count,
print "Blocks to targets."
