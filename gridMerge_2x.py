import math, bge, bpy, time
from mathutils import Vector


def roundGrid( vert, inc):
    
    
    return (round(vert[0]*inc)/inc,round(vert[1]*inc)/inc,round(vert[2]*inc)/inc)
 


def main():
    time1 = time.time()
    cont = bge.logic.getCurrentController()
    own = cont.owner 
    
    
    if 'ran' not in own:
        gridLocations = {}
        gridIndex = 0
        gridColors = {}
        gridNormal = {}
        gridAverage = {}
        gridUv = {}
        gridKey = {}
        polyMap = {}
        polyMapIndex = 0
        edges = []
        
        for obj in bpy.data.collections['cluster'].objects:
            go = 0
            mesh = obj.data
            for poly in mesh.polygons:
                polyLoc =  []
                
                for edgeKey in poly.edge_keys:
                    
                    #store edges as their locaiton rounded down as a tuple instead of index)
                    gridKey1 = roundGrid(obj.matrix_world @ mesh.vertices[edgeKey[0]].co, 100)
                    gridKey2 = roundGrid(obj.matrix_world @ mesh.vertices[edgeKey[1]].co, 100)
                    edges.append( ( gridKey1, gridKey2) )
                    
                    #create a key to be able to convert tupleLocKey back to vertex
                    if gridKey1 not in gridKey:
                        gridKey[gridKey1] = gridIndex
                        gridLocations[gridIndex] = gridKey1
                        gridIndex+=1
                    
                        
                    if gridKey2 not in gridKey:
                        gridKey[gridKey2] = gridIndex
                        gridLocations[gridIndex] = gridKey2
                        gridIndex+=1
                    
                    #gather faces tupleLocKeys         
                    if gridKey1 not in polyLoc:
                        polyLoc.append(gridKey1)
                    if gridKey2 not in polyLoc:
                        polyLoc.append(gridKey2)    
                        
                    if gridKey1 not in gridNormal:       
                        gridNormal[gridKey1] = obj.matrix_world @ mesh.vertices[edgeKey[0]].normal
                    
                    if gridKey2 not in gridNormal:       
                        gridNormal[gridKey2] = obj.matrix_world @ mesh.vertices[edgeKey[1]].normal
                        
                    
                #store face as tupleLocKeys        
                polyMap[polyMapIndex] = polyLoc
                polyMapIndex+=1     
                
                #store data about edge loop color, vertex color, normal later
             
        print('ran')
        
        #remap tupleLocKeys back to new index
        newPolygons = []
        index = 0
        
        
        for i in range(len(polyMap)):
            
            newPoly = []
            poly = polyMap[i]
            #print(poly)
            for vert in poly:
                newPoly.append(gridKey[vert])
            newPolygons.append(tuple(newPoly))
            
            
        #create vertex list in order
        vertexLocations = []
        for i in range(len(gridLocations)):
              data = gridLocations[i]
              vertexLocations.append(data)
        
        
        #convert edges tupleLocKey to index
        edgeN = []
        for edge in edges:
            edgeN.append( (gridKey[edge[0]],  gridKey[edge[1]])     )
        
        
        
        
        mesh_data = bpy.data.meshes.new("cube_mesh_data")
        mesh_data.from_pydata(vertexLocations, edgeN, newPolygons)

        newMesh = bpy.data.objects.new("Joined", mesh_data)  
        
        
        own['ran']=True
        print(time.time()-time1)
        for vert in newMesh.data.vertices:
           vert.normal = own.worldOrientation.inverted() @ gridNormal[gridLocations[vert.index]]
        print('set')    
        #for face in newMesh.data.polygons:
        #   face.use_smooth = True
        #newMesh.data.calc_normals()
        
        bpy.data.objects[own.name].data = newMesh.data
main()
       