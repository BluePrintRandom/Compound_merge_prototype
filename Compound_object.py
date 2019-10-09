import bpy, time
import bge
own = bge.logic.getCurrentController().owner
    

def select(collectionName, obName):
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
    
    print(bpy.context.selected_objects)
    bpy.ops.object.join() 
    
    copy = bpy.context.selected_objects[0].name
    bpy.data.scenes['Scene'].cursor.location = own.worldPosition
    bpy.data.scenes['Scene'].cursor.matrix = own.worldTransform
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.data.objects[own.name].data =  bpy.context.selected_objects[0].data.copy()
    bpy.data.objects[copy].select_set(True)
    
    
    bpy.ops.object.delete()
   
    for obj in bpy.context.selected_objects:
        bpy.data.objects[obj.name].select_set(False)
    
    bpy.data.scenes[0].view_layers[0].objects.active = bpy.data.objects[own.name]
  
    
    
    
    return
    
def merge_verts():
    
    bpy.data.scenes[0].view_layers[0].objects.active = bpy.data.objects[own.name]
    
    bpy.data.objects[own.name].select_set(True)
    print(bpy.context.selected_objects)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    
    
    

def main():
    key =bge.logic.getCurrentController().sensors['Key']
    if key.positive:
        start = time.time()
        own['Count']=0
        select('CollectionNew', own.name)
        merge()
        merge_verts()
        print(time.time() - start)
    
        
                 
main()
