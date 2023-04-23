from assets.managers import common
from assets.managers import constants
from assets.managers import entity,particle,ai,items
import os,random,json,pygame,math,pygame.gfxdraw
class Box():
    def __init__(self,rect):
        self.rect = rect
        self.hidden = False
        self.points = []
    def Draw(self,forcedraw=False):
        if not self.hidden or forcedraw: #check wheter or not the box is hidden, or if its being forced to draw
            neg_player_y = int(-common.player.y+4)  #unflip player y and the rect y positions
            player_x = int(common.player.x)+0.1
            player_y = int(common.player.y-4)
            point9 = None
            camera_height = common.loaded_level.camera_surface.get_height() #get camera values, used to keep the drawn polygons onscreen
            camera_width = common.loaded_level.camera_surface.get_width()
            camera_x = common.loaded_level.camera_surface.get_offset()[0]
            camera_y = common.loaded_level.camera_surface.get_offset()[1]
            e = common.loaded_level.camera_surface.get_rect() #prepare for checking whether or not the box is onscreen
            e.x = camera_x
            e.y = camera_y
            x = self.rect.x
            y = self.rect.y
            x2 = x+self.rect.w
            y2 = y+self.rect.h
            if self.rect.colliderect(e): #check if the box is onscreen
                if x<camera_x: #constrain the x and y to within the screen
                    x=camera_x-1
                if x2>camera_x+camera_width:
                    x2=camera_x+camera_width+1
                if y<camera_y:
                    y=camera_y-1
                if y2>camera_y+camera_height:
                    y2=camera_y+camera_height+1
                if player_x>x2: #prepare some x positions for the screen edges
                    x_value_1 = camera_x
                    x_value_2 = camera_x
                elif player_x>x and common.player.y>y2:
                    x_value_1 = camera_width+camera_x
                    x_value_2 = camera_x
                elif player_x>x and common.player.y<y:
                    x_value_1 = camera_x
                    x_value_2 = camera_width+camera_x
                else:
                    x_value_1 = camera_width+camera_x
                    x_value_2 = camera_width+camera_x
                if player_y<=y and player_x>=x2: #determine where the player is in relation to the box
                    point1 = (x,-y)              #then thats used to place the proper points on the box
                    point2 = (x2,-y2)
                    point8 = (x,y2)
                elif player_y>=y2+1 and player_x>=x2:
                    point1 = (x2,-y)
                    point2 = (x,-y2)
                    point8 = (x,y)
                elif player_y>=y2+1 and player_x<=x:
                    point1 = (x2,-y2)
                    point2 = (x,-y)
                    point8 = (x2,y)
                elif player_y<=y and player_x<=x:
                    point1 = (x,-y2)
                    point2 = (x2,-y)
                    point8 = (x2,y2)
                elif player_y<=y:
                    point1 = (x2,-y)
                    point2 = (x,-y)
                    point8 = (x2,y2)
                    point9 = (x, y2)
                elif player_x>x2:
                    point1 = (x2,-y)
                    point2 = (x2,-y2)
                    point8 = (x,y)
                    point9 = (x,y2)
                elif player_y>=y2+1:
                    point1 = (x,-y2)
                    point2 = (x2,-y2)
                    point8 = (x,y)
                    point9 = (x2,y)
                elif player_x<=x:
                    point1 = (x,-y2)
                    point2 = (x,-y)
                    point8 = (x2,y2)
                    point9 = (x2,y)
                else:
                    point1 = (x,-y)
                    point2 = (x,-y)
                    point8 = (x,y)
                slope2 = (point1[1]-neg_player_y)/(point1[0]-player_x) #compute the slopes, for use later
                slope1 = (point2[1]-neg_player_y)/(point2[0]-player_x)
                y_value1 = -(neg_player_y-((player_x-x_value_1)*slope1)) #compute the y values, using adjusted point-slope form
                y_value2 = -(neg_player_y-((player_x-x_value_2)*slope2)) #2 x values, a y value, and a slope
                if y_value1<=camera_y:  #check if the y values are offscreen, and if they are, set the y value within the screen
                    y_value1 = camera_y #and compute the x value for where that line intersects the y value
                    x_value_1 = player_x-((neg_player_y+camera_y)/slope1)
                elif y_value1>=camera_height+camera_y:
                    y_value1 = camera_height+camera_y
                    x_value_1 = player_x-((neg_player_y+camera_height+camera_y)/slope1)
                if y_value2<=camera_y:
                    y_value2 = camera_y
                    x_value_2 = player_x-((neg_player_y+camera_y)/slope2)
                elif y_value2>=camera_height+camera_y:
                    y_value2 = camera_height+camera_y
                    x_value_2 = player_x-((neg_player_y+camera_height+camera_y)/slope2)
                point1 = (point1[0],-point1[1]) #compensate for the reversed y-axis
                point2 = (point2[0],-point2[1])
                if point1==(x2,y):
                    point1 = (point1[0]-1,point1[1])
                elif point1==(x2,y2):
                    point1 = (point1[0]-1,point1[1]-1)
                elif point1==(x,y2):
                    point1 = (point1[0],point1[1]-1)
                if point2==(x2,y):
                    point2 = (point2[0]-1,point2[1])
                elif point2==(x2,y2):
                    point2 = (point2[0]-1,point2[1]-1)
                elif point2==(x,y2):
                    point2 = (point2[0],point2[1]-1)
                point3 = (x_value_1,y_value1) #write some points, these are the edge points
                point4 = (x_value_2,y_value2)
                points = [point1,point8]
                if point9!=None:
                    points.append(point9)
                points.append(point2)
                points.append(point3)
                if not (y_value1==y_value2 or x_value_1==x_value_2):  #adds extra points in the corners where needed, else there'll be a triangular gap
                    if (y_value1==camera_y and y_value2==camera_height+camera_y) or (y_value1==camera_height+camera_y and y_value2==camera_y): #whenever 1 y value leaves the screen and the other doesn't
                        if player_x>=x: #statements with 2 points being made account for the rare scenario in which points are on opposite edges
                            points.append((camera_x,camera_height+camera_y))
                            points.append((camera_x,camera_y))
                        else:
                            points.append((camera_width+camera_x,camera_y))
                            points.append((camera_width+camera_x,camera_height+camera_y))
                    elif (x_value_1==camera_x and x_value_2==camera_width+camera_x) or (x_value_1==camera_width+camera_x and x_value_2==camera_x):
                        if player_y>=y:                                       #account for points on adjacent edges
                            points.append((camera_width+camera_x,camera_y))
                            points.append((camera_x,camera_y))
                        else:
                            points.append((camera_x,camera_height+camera_y))
                            points.append((camera_width+camera_x,camera_height+camera_y))
                    elif y_value2==camera_y or y_value2==camera_height+camera_y: #accounts for the points being on adjacent edges
                        points.append((x_value_1,y_value2))
                    else:
                        points.append((x_value_2,y_value1))
                points.append(point4)
                self.points = points
                pygame.draw.polygon(constants.layer_4,(0,1,0),points)
                #draw the polygon (finally)
    def afterdraw(self,forcedraw=False):
        pass
        #if (not self.hidden or forcedraw) and len(self.points)>=3:
        #    pygame.gfxdraw.filled_polygon(constants.layer_4_a,self.points,(0,128,0,128))
class Edge():
    def __init__(self,pos1,pos2,facing):
        self.pos1 = pos1
        self.pos2 = pos2
        self.facing = facing
    def Draw(self,forcedraw=False):
        player_x = common.player.x
        player_y = common.player.y*-1+constants.layer_1.get_size()[1]
        camera_height = common.loaded_level.camera_surface.get_height() #get camera values, used to keep the drawn polygons onscreen
        camera_width = common.loaded_level.camera_surface.get_width()
        camera_x = common.loaded_level.camera_surface.get_offset()[0]
        camera_y = common.loaded_level.camera_surface.get_offset()[1]
        if (not forcedraw) and (constants.layer_1.get_bounding_rect().collidepoint(self.pos1[0],self.pos1[1]) or constants.layer_1.get_bounding_rect().collidepoint(self.pos2[0],self.pos2[1])):
            points = [self.pos1,self.pos2]
            if self.facing==0 and common.player.y>=self.pos1[0]:
                if not player_x==self.pos1[0] and not player_x==self.pos2[0]:
                    if player_x<=self.pos1[0]:
                        x_1 = camera_x+camera_width
                        x_2 = camera_x+camera_width
                    slope1 = (self.pos1[1]-player_y)/(self.pos1[0]-player_x)
                    slope2 = (self.pos2[1]-player_y)/(self.pos2[0]-player_x)
                    y_1 = -(player_y-((player_x-x_1)*slope1)) #compute the y values, using adjusted point-slope form
                    y_2 = -(player_y-((player_x-x_2)*slope2))
                    points.append((x_2,y_2),(x_1,y_1))
                    pygame.draw.polygon(constants.layer_4,(0,1,0),points)
class Background():
    def __init__(self,data:dict,image:pygame.Surface)->None:
        self.scroll_x = data.get("scroll_x",0)
        self.scroll_y = data.get("scroll_y",0)
        self.x = data.get("x",0)
        self.y = data.get("y",0)
        self.motion_x = data.get("motion_x",0)
        self.motion_y = data.get("motion_y",0)
        self.ticker_x = common.Ticker(image.get_width())
        self.ticker_y = common.Ticker(image.get_height())
        self.ticker_x.Trigger()
        self.ticker_y.Trigger()
        self.image = image
        self.rooms = data.get("rooms",[])
    def get_background(self,rect:pygame.Rect)->pygame.Surface:
        self.ticker_x.Loop(self.motion_x)
        self.ticker_y.Loop(self.motion_y)
        surface = pygame.Surface((rect.w,rect.h))
        for i in range(-2,math.ceil(rect.w/self.image.get_width())+1):
            for j in range(-2,math.ceil(rect.h/self.image.get_height())+1):
                surface.blit(self.image,(i*self.image.get_width()-rect.x+int(common.loaded_level.camera[0]*self.scroll_x%self.image.get_width()+self.ticker_x.tick),j*self.image.get_height()-rect.y+int(common.loaded_level.camera[1]*self.scroll_y%self.image.get_height()+self.ticker_y.tick)))
        #print(2*self.image.get_width()-rect.x+int(common.player.x*self.scroll_x+self.ticker_x.tick))
        return surface
class UnloadedLevel():
    def __init__(self,level_id,pos):
        self.level_id = level_id
        possible_rooms = []
        for i in common.backgrounds:
            for j in i.rooms:
                if j==level_id:
                    possible_rooms.append(i)
        if len(possible_rooms)>1:
            self.background = possible_rooms[random.randint(0,len(possible_rooms)-1)]
        elif len(possible_rooms)==0:
            self.background = Background({"rooms":[self.level_id]},pygame.Surface((100,100)))
        else:
            self.background = possible_rooms[0]
        possible_rooms = []
        for i in common.MusicLibrary.values():
            for j in i.levels:
                if j==self.level_id:
                    possible_rooms.append(i)
        if len(possible_rooms)==0:
            possible_rooms.append(common.MusicLibrary["test"])
        self.music = possible_rooms
        self.pos = pos
    def load(self):
        common.global_position = [self.pos[0],self.pos[1]]
        common.loaded_level.load(self.music,self.level_id,self.background)
class Level():
    def __init__(self):
        self.name = "simple"
        self.camera_surface = constants.layer_4.subsurface(0,0,constants.CAM_WIDTH,constants.CAM_HEIGHT)
        self.camera = [0,0]
    def play_music(self):
        if len(self.music)>1:
            self.music[random.randint(0,len(self.music)-1)].play_music()
        else:
            self.music[0].play_music()
    def load(self,music,levelname="test",background=None):
        self.music = music
        #self.play_music()
        self.name = levelname
        if background==None:
            background = Background({"rooms":[self.name]},pygame.Surface((100,100)))
        self.background = background
        path = open(os.path.join("assets","levels",levelname,"data.json"))
        if os.path.exists(os.path.join("assets","levels",levelname,"data.json")):
            data = json.load(path)      #load level data.json, next few lines load collision and display from one or both files
        else:
            raise FileNotFoundError("the \'data\' file for "+levelname+" could not be found")
        if [os.path.exists(os.path.join("assets","levels",levelname,"display.png")) and os.path.exists(os.path.join("assets","levels",levelname,"collision.png"))]==[False,False]:
            raise FileNotFoundError("both the \'collision\' and \'display\' files are missing from "+levelname+", at least one must be present")
        elif not os.path.exists(os.path.join("assets","levels",levelname,"display.png")): #load from collision file if display file doesnt exist
            self.display_texture = pygame.image.load(os.path.join("assets","levels",levelname,"collision.png"))
            self.display_texture = pygame.transform.scale(self.display_texture,(self.display_texture.get_width()*data["level_scale"],self.display_texture.get_height()*data["level_scale"]))
            self.collision_texture = self.display_texture.copy()
        elif not os.path.exists(os.path.join("assets","levels",levelname,"collision.png")): #load from display file if collision file doesnt exist
            self.display_texture = pygame.image.load(os.path.join("assets","levels",levelname,"display.png"))
            self.display_texture = pygame.transform.scale(self.display_texture,(self.display_texture.get_width()*data["level_scale"],self.display_texture.get_height()*data["level_scale"]))
            self.collision_texture = self.display_texture.copy()
        else: #if both files are present, load normally
            self.display_texture = pygame.image.load(os.path.join("assets","levels",levelname,"display.png"))
            self.collision_texture = pygame.image.load(os.path.join("assets","levels",levelname,"collision.png"))
            self.collision_texture = pygame.transform.scale(self.collision_texture,(self.collision_texture.get_width()*data["level_scale"],self.collision_texture.get_height()*data["level_scale"]))
        self.collision = pygame.mask.from_surface(self.collision_texture) #make collision
        self.camera = [0,0]                                               #make camera
        constants.layer_1 = pygame.transform.scale(constants.layer_1,(self.display_texture.get_size()))
        constants.layer_2 = pygame.transform.scale(constants.layer_1,(self.display_texture.get_size()))
        constants.layer_3 = pygame.transform.scale(constants.layer_1,(self.display_texture.get_size()))
        constants.layer_4 = pygame.transform.scale(constants.layer_1,(self.display_texture.get_size()))
        constants.layer_4_a = pygame.transform.scale(constants.layer_1,(self.display_texture.get_size())) #make the main level surface from the display texture
        self.camera_surface = constants.layer_4.subsurface(0,0,constants.CAM_WIDTH,constants.CAM_HEIGHT) #make the camera, which is a subsurface of the level surface
        common.boxes.clear()                      #clear out various lists, in case they have stuff left over from the previous level
        common.delparticles.extend(common.particles.keys())
        common.delentities.extend(common.entities.keys())
        try:
            for i in data["boxes"]:
                common.NewThing(Box(pygame.Rect(i["x"],i["y"],i["w"],i["h"])),common.boxes) #add extra boxes w/o collision
        except:
            pass
        try:
            for i in data["level_transitions"]:
                if i["style"]=="old":
                    common.NewThing(entity.TransitionObject(pygame.Rect(i["x"],i["y"],i["w"],i["h"]),(i["dest_x"],i["dest_y"]),i["dest_level"]),common.newentities) #add level transitions
                elif i["style"]=="new":
                    common.NewThing(entity.DynamicTransitionObject(pygame.Rect(i["x"],i["y"],i["w"],i['h']),i["transition_id"],(i["dest_x"],i["dest_y"]),common.global_position),common.newentities)
        except:
            pass
        try:
            for i in data["enemies"]:
                if i.get("always_spawns",False): #add enemies with the always_spawns tag as true, defaults to false
                    entity.new_entity(i["x"],i["y"],i["hp"],i["type"]) #add enemies
        except:
            pass
        print(common.newentities)
        if data.get("particle_spawners",None)!=None:
            for i in data["particle_spawners"]:
                common.NewThing(particle.ParticleArea(pygame.Rect(i["x"],i["y"],i["w"],i["h"]),i["freq"],i["color"],i["behavior"],i["duration"],i["variation"]))
        k=0
        m=0
        '''edgelist = []
        self.collision.invert()
        collision_objects = self.collision.connected_components()
        for object in collision_objects:
            x=0
            y=0
            finding_point = True
            while finding_point:
                x+=1
                if common.out_of_bounds((x,y)):
                    x=0
                    y+=1
                if object.get_at((x,y))>=1:
                    finding_point = False
            print((x,y))
            start = [x,y]
            point = (x,y)
            pos = [x+1,y]
            prev_pos = [x,y]
            direction = 1
            while pos!=start:
                prev_pos = [pos[0],pos[1]]
                print(pos)
                if not common.out_of_bounds((x,y-1)):
                    up = object.get_at((x,y-1))
                else:
                    up = 0
                if not common.out_of_bounds((x,y+1)):
                    down = object.get_at((x,y+1))
                else:
                    down = 0
                if not common.out_of_bounds((x+1,y)):
                    right = object.get_at((x+1,y))
                else:
                    right = 0
                if not common.out_of_bounds((x-1,y)):
                    left = object.get_at((x-1,y))
                else:
                    left = 0
                if up==0 and right==1 and down==1 and left==1:
                    pos[0]+=1
                elif up==1 and right==1 and down==0 and left==1:
                    pos[0]-=1
                elif up==1 and right==0 and down==1 and left==1:
                    pos[1]+=1
                elif up==1 and right==1 and down==1 and left==0:
                    pos[1]-=1
                elif up==0 and right==0 and down==1 and left==1:
                    edgelist.append(Edge(point,pos,2))
                    print("2")
                    point = (pos[0],pos[1])
                    pos[1]+=1
                    direction = 2
                elif up==1 and right==0 and down==0 and left==1:
                    edgelist.append(Edge(point,pos,3))
                    print("3")
                    point = (pos[0],pos[1])
                    pos[0]-=1
                    direction = 3
                elif up==1 and right==1 and down==0 and left==0:
                    edgelist.append(Edge(point,pos,0))
                    print("0")
                    point = (pos[0],pos[1])
                    pos[1]-=1
                    direction = 0
                elif up==0 and right==1 and down==1 and left==0:
                    edgelist.append(Edge(point,pos,1))
                    print("1")
                    point = (pos[0],pos[1])
                    pos[0]+=1
                    direction = 1
                elif up==1 and right==1 and down==1 and left==1:
                    if direction<3:
                        edgelist.append(Edge(point,pos,direction+1))
                        print(direction+1)
                    else:
                        edgelist.append(Edge(point,pos,0))
                        print("0")
                    point = (pos[0],pos[1])
                    if direction==0:
                        direction=3
                        pos[0]-=1
                    elif direction==1:
                        direction=0
                        pos[1]-=1
                    elif direction==2:
                        direction=1
                        pos[0]+=1
                    else:
                        direction=2
                        pos[1]+=1
                if (pos==prev_pos) or common.out_of_bounds(pos):
                    raise RuntimeError("Edge finder hung at "+str(pos))

        self.collision.invert()'''
        boxrectlist = []                                                     #all this is the algorithm for making the boxes
        for i in range(0,self.collision_texture.get_width()-1):              #for each x
            for j in range(0,self.collision_texture.get_height()-1):         #for each y
                rect = pygame.Rect(i,j,1,1)
                if rect.collidelist(boxrectlist)==-1 and self.collision.get_at((i,j))==1: #check the point isnt already in a box
                    newbox= pygame.Rect(i,j,1,1)  #make a box
                    k=0
                    while True:
                        if newbox.x+k<constants.layer_1.get_width()-1:         #go as far right as possible
                            if self.collision.get_at((newbox.x+k,j))==0:
                                break
                        else:
                            break
                        if k>constants.MAX_RECT_SIZE:
                            break
                        k+=1
                    newbox.w=k #set the width
                    newbox.h=constants.layer_1.get_height()-newbox.y-1
                    for l in range(newbox.x,newbox.x+newbox.w):         #go as far down as possible, keeping the shortest column for the height
                        m=0
                        while True:
                            if not (l>constants.layer_1.get_width()-1 or newbox.y+m>constants.layer_1.get_height()-1):
                                if self.collision.get_at((l,newbox.y+m))==0:
                                    break
                            else:
                                break
                            if m>=newbox.h or m>constants.MAX_RECT_SIZE:
                                break
                            m+=1
                        newbox.h=m
                    if not (newbox.w==0 or newbox.h==0): #check that the rect isnt invalid
                        boxrectlist.append(newbox)       #then add the box
        #print(len(edgelist))
        #for i in edgelist:
        #    common.NewThing(i,common.boxes)
        for i in boxrectlist:     #for every rect in the box list, make an actual Box class
            common.NewThing(Box(i),common.boxes)
        getattr(common.run,common.current_map+"_map").blit(getattr(common.run,common.current_map).map.subsurface(pygame.Rect(common.global_position[0]-1,common.global_position[1]-1,3,3)),(common.global_position[0]-1,common.global_position[1]-1))
    def update_camera(self,pos=None):
        if pos!=None:                #make a hook for placing the camera wherever
            self.camera[0] = pos[0]
            self.camera[1] = pos[1]
        else:
            self.camera = [int(common.player.x-(constants.CAM_WIDTH/2)),int(common.player.y-(constants.CAM_HEIGHT/2))] #set the camera to put the player in the middle
        if self.camera[0]<=0:          #constrain the camera to within the level borders, else game crash
            self.camera[0] = 0
        if self.camera[0]+constants.CAM_WIDTH>=constants.layer_1.get_width():
            self.camera[0] = constants.layer_1.get_width()-constants.CAM_WIDTH
        if self.camera[1]<=0:
            self.camera[1] = 0
        if self.camera[1]+constants.CAM_HEIGHT>=constants.layer_1.get_height():
            self.camera[1] = constants.layer_1.get_height()-constants.CAM_HEIGHT
        self.camera_surface = constants.layer_4.subsurface(self.camera[0],self.camera[1],constants.CAM_WIDTH,constants.CAM_HEIGHT) #update the camera subsurface
        self.camera_surface.get_view()
class Node():
    def __init__(self,pos,type,maxconnections,owner): #not really used, might be used later
        self.pos = pos
        self.type = type
        self.maxconnections = maxconnections
        self.owner = owner
        self.connections = []
    def check(self,node):
        made_connection = False
        if len(self.connections)<self.maxconnections and len(node.connections)<node.maxconnections and self.connections.count(node)==0:
            self.connections.append(node)
            node.connections.append(self)
            self.owner.path(self.pos,node.pos)
            made_connection = True
        return made_connection
class Map():
    def GrowingTree(surface,extraconnections=1000): #maze generation algorithm
        pos = (random.randint(0,int(surface.get_width()/2))*2-1,random.randint(0,int(surface.get_height()/2))*2-1)
        allvisited = [pos]
        visited = [pos]
        while visited!=[]:
            valid_pos = [False,False,False,False]
            if pos[1]-2>0: #check the positions around it to see if they were visited
                if allvisited.count((pos[0],pos[1]-2))==0:
                    valid_pos[0]=True
            if pos[0]+2<surface.get_width():
                if allvisited.count((pos[0]+2,pos[1]))==0:
                    valid_pos[1]=True
            if pos[1]+2<surface.get_height():
                if allvisited.count((pos[0],pos[1]+2))==0:
                    valid_pos[2]=True
            if pos[0]-2>0:
                if allvisited.count((pos[0]-2,pos[1]))==0:
                    valid_pos[3]=True
            if valid_pos==[False,False,False,False]: #if all tiles adjacent are visited, remove from the visited list
                visited.remove(pos)
            else:
                while True: #else, randomly choose a valid pos and advance in that direction
                    value = random.randint(0,3)
                    if value==0 and valid_pos[0]:
                        newpos = (pos[0],pos[1]-2)
                        break
                    elif value==1 and valid_pos[1]:
                        newpos = (pos[0]+2,pos[1])
                        break
                    elif value==2 and valid_pos[2]:
                        newpos = (pos[0],pos[1]+2)
                        break
                    elif value==3 and valid_pos[3]:
                        newpos = (pos[0]-2,pos[1])
                        break
                    if valid_pos==[False,False,False,False]:
                        break
                visited.append(newpos)
                allvisited.append(newpos)
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,newpos)
            if random.random()<=0.3 and len(visited)>0: #allow branches by allowing random teleportation
                pos = visited[random.randint(0,len(visited)-1)]
            else:
                if len(visited)>0: #most of the time, it will continue with the previous position
                    pos = visited[len(visited)-1]
        for i in range(0,extraconnections): #mess up the perfect maze by splattering with random connections
            pos = (random.randint(3,int(surface.get_width()/2))*2-3,random.randint(3,int(surface.get_height()/2))*2-3)
            value = random.randint(0,3)
            if value==0:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0],pos[1]-2))
            elif value==1:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0],pos[1]+2))
            elif value==2:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0]-2,pos[1]))
            else:
                pygame.draw.line(surface,constants.PATH_TILE_COLOR,pos,(pos[0]+2,pos[1]))
        return surface
    def __init__(self,seed,type=0):
        self.seed = seed
        self.type = type
        if self.type==0: #intermediary type
            self.map = pygame.Surface((99,99))
            self.map.fill(constants.MAP_BACKGROUND_COLOR)
            self.doorways = []
            self.doorways.append([49,49]) #start tile pos
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(5,15)-1]) #memory tile pos
            self.doorways.append([2*random.randint(20,30)-1,2*random.randint(5,15)-1]) #dream tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(5,15)-1]) #labyrinth tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(20,30)-1]) #fracture tile pos
            self.doorways.append([2*random.randint(35,45)-1,2*random.randint(35,45)-1]) #abstract tile pos
            self.doorways.append([2*random.randint(20,30)-1,2*random.randint(35,45)-1]) #abyss tile pos
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(35,45)-1]) #trauma tile pos, not what it seems
            self.doorways.append([2*random.randint(5,15)-1,2*random.randint(20,30)-1]) #awakening tile pos
            self.doorways.append([2*random.randint(30,35)-1,2*random.randint(20,30)-1]) #auric door tile pos, also the end of the game
            for i in range(len(self.doorways)): #make the pos' into Node objects
                self.doorways[i] = Node(self.doorways[i],"doorway",2,self)
            self.secretrooms = [] #secret rooms (orange tiles)
            for i in range(random.randint(3,6)):
                while True:
                    point = [2*random.randint(5,45)-1,2*random.randint(5,45)-1]
                    if self.map.get_at(point)==constants.MAP_BACKGROUND_COLOR:
                        break
                self.secretrooms.append(Node(point,"secret",1,self))
            self.map.blit(Map.GrowingTree(self.map,600),(0,0)) #generate the maze
            for i in self.secretrooms:                     #make sure secret rooms only have 1 tile connection
                self.map.set_at(i.pos,constants.SECRET_ROOM_TILE_COLOR)
                value = random.randint(0,3)
                self.map.set_at((i.pos[0]-1,i.pos[1]),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0],i.pos[1]-1),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0],i.pos[1]+1),constants.MAP_BACKGROUND_COLOR)
                self.map.set_at((i.pos[0]+1,i.pos[1]),constants.MAP_BACKGROUND_COLOR)
                if value==0:
                    self.map.set_at((i.pos[0]-1,i.pos[1]),constants.PATH_TILE_COLOR)
                elif value==1:
                    self.map.set_at((i.pos[0],i.pos[1]-1),constants.PATH_TILE_COLOR)
                elif value==2:
                    self.map.set_at((i.pos[0],i.pos[1]+1),constants.PATH_TILE_COLOR)
                else:
                    self.map.set_at((i.pos[0]+1,i.pos[1]),constants.PATH_TILE_COLOR)
            self.map.set_at(self.doorways[0].pos,constants.START_TILE_COLOR) #start tile
            self.map.set_at(self.doorways[1].pos,constants.MEMORY_TILE_COLOR) #memory tile
            self.map.set_at(self.doorways[2].pos,constants.DREAM_TILE_COLOR) #dream tile
            self.map.set_at(self.doorways[3].pos,constants.LABYRINTH_TILE_COLOR) #labyrinth tile
            self.map.set_at(self.doorways[4].pos,constants.FRACTURE_TILE_COLOR) #fracture tile
            self.map.set_at(self.doorways[5].pos,constants.ABSTRACT_TILE_COLOR) #abstract tile
            self.map.set_at(self.doorways[6].pos,constants.ABYSS_TILE_COLOR) #abyss tile
            self.map.set_at(self.doorways[7].pos,constants.TRAUMA_TILE_COLOR) #trauma tile
            self.map.set_at(self.doorways[8].pos,constants.AWAKENING_TILE_COLOR) #awakening tile
            self.map.set_at(self.doorways[9].pos,constants.AURIC_DOOR_TILE_COLOR) #auric door tile
            self.map.set_at((self.doorways[0].pos[0]-1,self.doorways[0].pos[1]),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0],self.doorways[0].pos[1]-1),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0],self.doorways[0].pos[1]+1),constants.MAP_BACKGROUND_COLOR)
            self.map.set_at((self.doorways[0].pos[0]+1,self.doorways[0].pos[1]),constants.PATH_TILE_COLOR)
            pygame.draw.rect(self.map,constants.PATH_TILE_COLOR,pygame.Rect(self.doorways[0].pos[0]-2,self.doorways[0].pos[1]-2,5,5),1)
            self.levelarray = {}
            for i in range(1,int(self.map.get_width()/2)*2,2):
                for j in range(1,int(self.map.get_height()/2)*2,2):
                    if self.map.get_at((i,j))!=constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j))!=constants.SECRET_ROOM_TILE_COLOR:
                        if self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("t_bottom",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("t_top",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("t_right",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("t_left",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("straight_y",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("straight_x",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("L_top_left",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("L_top_right",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("L_bottom_left",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("L_bottom_right",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("end_up",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("end_right",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("end_down",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("end_left",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i+1,j))==constants.PATH_TILE_COLOR and self.map.get_at((i,j-1))==constants.PATH_TILE_COLOR and self.map.get_at((i,j+1))==constants.PATH_TILE_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("cross",(i,j))})
                        elif self.map.get_at((i-1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i+1,j))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j-1))==constants.MAP_BACKGROUND_COLOR and self.map.get_at((i,j+1))==constants.MAP_BACKGROUND_COLOR:
                            self.levelarray.update({str((i,j)):UnloadedLevel("empty",(i,j))})
                        else:
                            print("up: "+str(self.map.get_at((i,j-1)))+", right: "+str(self.map.get_at((i+1,j)))+", down: "+str(self.map.get_at((i,j+1)))+", left: "+str(self.map.get_at((i-1,j))))
                            raise ValueError("invalid level map shape at "+str(i)+", "+str(j))
            self.levelarray.update({str((self.doorways[0].pos[0],self.doorways[0].pos[1])):UnloadedLevel("start",self.doorways[0].pos)})
            common.global_position = [self.doorways[0].pos[0],self.doorways[0].pos[1]]
class Run():
    def __init__(self):
        self.seed = 0
        self.difficulty = 0
        self.intermediary = None
        self.intermediary_map = None
    def reload(self,difficulty,seed=0x00000000): #this object will be saved
        self.seed = seed
        common.player.x = constants.DEF_START_POS[0]
        common.player.y = constants.DEF_START_POS[1]
        common.player.AIpointer = ai.playerAI
        common.player.overlay_active = True
        common.player.inventory["main_0"] = items.items["gun"]
        common.player.inventory["main_1"] = items.items["gun2"]
        common.player.facing_away = True
        common.current_map = "intermediary"
        random.seed(self.seed)
        self.difficulty = difficulty
        self.intermediary = Map(self.seed)
        self.intermediary_map = pygame.Surface((self.intermediary.map.get_width(),self.intermediary.map.get_height()))
        self.intermediary_map.fill(constants.MAP_BACKGROUND_COLOR)
        self.intermediary.levelarray[str((self.intermediary.doorways[0].pos[0],self.intermediary.doorways[0].pos[1]))].load()