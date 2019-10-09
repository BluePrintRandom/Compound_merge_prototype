import bpy
import bge
own = bge.logic.getCurrentController().owner
    

def select(collectionName, obName):
    #duplicate and merge
    
    #deselect selected
    
    
   
    for obj in bpy.context.selected_objects:
        bpy.data.objects[obj.name].select_set(False)
   
    
    
    objs = []   
    #select objects to merge   
    for obj in  bpy.data.collections[collectionName].objects:
        
        ob = obj.copy()
        # link to collection if need be
        print(bpy.data.collections)
        bpy.data.collections['Collection 1'].objects.link(ob)
        objs.append(ob)
        
    for obj in objs:
        obj.select_set(True)     
    
         
         
    bpy.data.scenes[0].view_layers[0].objects.active = obj         
        
def merge():    
    
    #set active object to one of the objects being used    
    #bpy.context.view_layer.objects.active = obj    
    
    
    #should print [objects] 
    print(bpy.context.selected_objects)
    #bpy.ops.object.duplicate(linked=False, mode='INIT')
    bpy.ops.object.join() 
    
    #bpy.ops.mesh.merge(  
    
    
    copy = bpy.context.selected_objects[0].name
    
    bpy.data.objects[own.name].data =  bpy.context.selected_objects[0].data.copy()
    bpy.data.objects[copy].select_set(True)
    
    
    bpy.ops.object.delete()
    #says it's deleting this in the console
    bpy.data.objects[own.name].select_set(True)
    
    
    
    return
    
       
    
    

def main():
    own['Count']=0
    select('MeshCollection1', own.name)
    merge()
    
        
                 
main()
