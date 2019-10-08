import bge,bpy,mathutils, time
from mathutils import Vector


#round vector to grid
def roundGrid(vect, int):
    return (round(vect[0]*int)/int,round(vect[1]*int)/int, round(vect[2]*int)/int )



def main():

    cont = bge.logic.getCurrentController()
    own = cont.owner
    #blender game engine mouse over sensor
    mo = cont.sensors['MouseOver']
    
    
    if 'Connects' not in own:
        #begin measure time
        time1 = time.time()
        
        
        
        #gather objects to merge - this will use a collection later
        mergeList = []
        for obj in own.scene.objects:
            if 'Collection' in obj:
                mergeList.append(obj)
        
        
        #loop over each polygons edge_loops and build a table of them where instead of a index we use a point in space
        #subsequent calls of loop will add more edges to vertex that overlap
        
        
        # 1/inc is grid incriment
        inc = .001
        
        inc = 1/inc
        
        #inc = 100
        Connects = {}
        Colors = {}
        UVs = {}
        Normals = {}
        for obj in mergeList:
            mesh = bpy.data.objects[obj.name]
            colors = mesh.data.vertex_colors[0].data
            uvs = mesh.data.uv_layers[0].data
            for poly in mesh.data.polygons:
                for loop in poly.loop_indices:
                    loop = mesh.data.loops[loop]
                    key = roundGrid(obj.worldTransform @ mesh.data.vertices[loop.vertex_index].co, 200)
                    poz = obj.worldTransform @ mesh.data.vertices[loop.vertex_index].co
                    data = [(key,poz) ]
                    uvData = [(uvs[loop.index].uv, poz.magnitude) ]
                    colorData  = [(colors[loop.index].color, poz.magnitude) ] 
                    
                    for loop2 in poly.loop_indices:
                        loop2 = mesh.data.loops[loop2]
                        
                        if loop2!=loop:
                            poz2 = obj.worldTransform @  mesh.data.vertices[loop2.vertex_index].co
                            data.append( ( roundGrid(poz2, 200), poz2 ) )
                            colorData.append( (colors[loop2.index].color, poz2 ))
                            uvData.append( (uvs[loop2.index].uv, poz2) )
                            
                            
                    data.sort(key=lambda x: x[1])       
                    colorData.sort(key =lambda x: x[1])
                    uvData.sort(key=lambda x: x[1])
                    
                    d2 = []
                    dc = []
                    u2 = []
                    for entry in data:
                        d2.append(entry[0])
                    for entry in colorData:
                        dc.append(entry[0])
                    for entry in uvData:
                        u2.append(entry[0])
                                
                    
                    if key not in Connects:        
                        Connects[key] = [ d2 ]
                        Colors[key] = [dc]
                        UVs[key] = [u2]
                        Normals[key] = mesh.data.vertices[loop.vertex_index].normal
                        
                    else:
                        if d2 not in Connects[key]:
                            Connects[key].append(d2)
                            Colors[key].append(dc)
                            UVs[key].append(u2)
                            n = mesh.data.vertices[loop.vertex_index].normal
                            n = (n+  Normals[key]) *.5
                            Normals[key] = n.normalized()
                            
                           
                            
                   
        
        kdl = {}                    
        kdTree = mathutils.kdtree.KDTree(len(Connects))
        index =0           
        for connect in Connects:
            kdl[index] = connect
            kdTree.insert( Vector(connect),index)
            index+=1
        kdTree.balance()
        own['KD']=kdTree   
        own['Connects'] = Connects 
        own['kdl'] = kdl
        own['Count']=0
        print('time elapsed')
        v = time.time() - time1
        print(v)
    elif mo.positive:
        #own['placed']=True
        
        index = own['KD'].find(mo.hitPosition)
        #print('hit '+str(index[1]))
        
        key = own['kdl'][index[1]]
        #print(key)
        
        data = own['Connects'][key]
        #print(data)
        
        for entry in data:
            #print(entry)
            index = 0
            for i in range(len(entry)):
                point = entry[i-1]
                
                
                if i!=0:
                    #print(point)
                    #print(point1)
                    line = own.scene.addObject('Line',own,15)
                    line.worldPosition = Vector(point)
                    p2 = entry[index-1]
                    v2 = (Vector(point) - Vector(p2))
                    line.alignAxisToVect(-v2.normalized(),1,1)
                    line.localScale = [1, v2.magnitude,1]
                    #print("added")
                
             
             
        
        
             
                
                
            
            

main()
