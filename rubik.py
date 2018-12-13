import numpy as np
import cv2
import imutils

#set the lists for all 6 sides to white for initialize
top= ("W", "W", "W", "W", "W", "W", "W", "W", "W")
bottom=("W","W","W","W","W","W","W","W","W")
left=("W","W","W","W","W","W","W","W","W")
right=("W","W","W","W","W","W","W","W","W")
front=("W","W","W","W","W","W","W","W","W")
back=("W","W","W","W","W","W","W","W","W")

#set flags that all side are not completed
top_complete= False
bottom_complete = False
left_complete = False
right_complete = False
front_complete = False
back_complete = False

#set counters for all 6 colors to 0 for initialize
wcount = 0
bcount = 0
rcount = 0
gcount = 0
ycount = 0
ocount = 0

rubik_net = np.zeros((196,261,3), np.uint8)


#routine for counting number of each color that has appeaded on each face. Used at the end to ensure there is 9 of each colour before exiting
def count_colours (fcheck, countall):
    (wcount,bcount,rcount,gcount,ycount,ocount)=countall
    for pos in range (9):
        if fcheck[pos]=="W":
            wcount +=1
        elif fcheck[pos] == "B":
            bcount +=1
        elif fcheck[pos] == "R":
            rcount+=1
        elif fcheck[pos] == "G":
            gcount+=1
        elif fcheck[pos] == "Y":
            ycount+=1
        elif fcheck[pos] == "O":
            ocount+=1
    countall=(wcount,bcount,rcount,gcount,ycount,ocount)
    return countall


#routine for drawing the read faces on the screen
def draw_face(colorss,x,y,m): 
    toprow = colorss[0:3]
    midrow = colorss[3:6]
    lastrrow = colorss[6:9]
    tile_color = (0,0,0)
    #draw a black square as background
    if m == 1:
        cv2.rectangle(rubik_net, (0+x,0+y ), (65+x, 65+y), (0,0,0),-1)
    elif m == 2:
        cv2.rectangle(image, (0+x,0+y ), (65+x, 65+y), (0,0,0),-1)
    
 
    #draw the coloured squares for top row
    for pos in range(3):
        if toprow[pos] == "W":
            tile_color = (255,255,255)
        elif toprow[pos] == "G":
            tile_color = (0,255,0)
        elif toprow[pos] == "B":
            tile_color = (255,0,0)
        elif toprow[pos] == "R":
            tile_color = (0,0,255)
        elif toprow[pos] == "O":
            tile_color = (0,100,255)
        elif toprow[pos] == "Y":
            tile_color = (50,255,255)   
        elif toprow[pos] == "N":
            tile_color = (0,0,0)
        if m == 1:
            cv2.rectangle((rubik_net), (20*pos+5+x,5+y ), (20*pos+20+x, 20+y), tile_color,-1)
        elif m == 2:
            cv2.rectangle((image), (20*pos+5+x,5+y ), (20*pos+20+x, 20+y), tile_color,-1)
 
    #draw the coloured squares for middle row 
    for pos in range(3):
        if midrow[pos] == "W":
            tile_color = (255,255,255)
        elif midrow[pos] == "G":
            tile_color = (0,255,0)
        elif midrow[pos] == "B":
            tile_color = (255,0,0)
        elif midrow[pos] == "R":
            tile_color = (0,0,255)
        elif midrow[pos] == "O":
            tile_color = (0,100,255)
        elif midrow[pos] == "Y":
            tile_color = (50,255,255)
        elif middle_row[pos] == "N":
            tile_color = (0,0,0)
        if m == 1:
            cv2.rectangle((rubik_net), (20*pos+5+x,25+y ), (20*pos+20+x, 40+y), tile_color,-1)
        elif m == 2:
            cv2.rectangle((image), (20*pos+5+x,25+y ), (20*pos+20+x, 40+y), tile_color,-1)
        

    #draw the coloured squares for bottom row  
    for pos in range(3):
        if lastrrow[pos] == "W":
            tile_color = (255,255,255)
        elif lastrrow[pos] == "G":
            tile_color = (0,255,0)
        elif lastrrow[pos] == "B":
            tile_color = (255,0,0)
        elif lastrrow[pos] == "R":
            tile_color = (0,0,255)
        elif lastrrow[pos] == "O":
            tile_color = (0,100,255)
        elif lastrrow[pos] == "Y":
            tile_color = (50,255,255)
        elif lastrrow[pos] =="N":
            tile_color = (0,0,0)
        if m == 1:
            cv2.rectangle((rubik_net), (20*pos+5+x,45+y ), (20*pos+20+x, 60+y), tile_color,-1)
        elif m == 2:
            cv2.rectangle((image), (20*pos+5+x,45+y ), (20*pos+20+x, 60+y), tile_color,-1)


#Main loop for processing the 6 images
for side in range(6):
    
    if side == 0:
        image = cv2.imread("1.png") 
    elif side == 1:
        image = cv2.imread("2.png") 
    elif side == 2:
        image = cv2.imread("3.png") 
    elif side == 3:
        image = cv2.imread("4.png") 
    elif side == 4:
        image = cv2.imread("5.png") 
    elif side == 5:
        image = cv2.imread("6.png")
    
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blurred, 85, 255, cv2.THRESH_BINARY)[1]
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # loop over the contours
    candidates=[]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
 
        # if the shape has 4 vertices, it is either a square or a rectangle
        if len(approx) == 4:
            # compute the bounding box of the contour and use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
 
            # a square will have an aspect ratio that is approximately 1
            if ar > .7 and ar < 1.3 :       
                candidates.append((x,y,w,h))
        
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
             
                # draw the contour of the candidates in the image for debugging purposes
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
     
    new=candidates
    #loop through all the countours in the candidantes list 
    for d in new:
        neighbors=0
        (x,y,w,h) = d
        for (x2,y2,w2,h2) in new:
        #count how many neighbors each countour in candidanteslist has which are closer than width * 3.5 
            if abs(x-x2) < (w*3.5) and abs(y-y2) < (h*3.5):
                neighbors +=1
            #remove any candidantes with less than 5 neighbors    
        if neighbors < 5 :   
            candidates.remove(d)
           
    #sort candidates if there's 9 of them
    tmp=[]  
    if len(candidates)==9 :
        #Write to tmp the center y,x of candidantes so that we can sort in y direction
        for (x3,y3,w3,h3) in candidates:     
            tmp.append( (y3+(h/2), x3+(w/2)) )     
        tmp = sorted(tmp)
        #cut into sets of 3 i.e the 3 rows of colours
        top_row=tmp[0:3]
        tmp = tmp[3:9]
        tmp = sorted(tmp)
        middle_row = tmp[0:3]
        bottom_row = tmp[3:6]
     
        #sort top_row
        temp_row=[]
        #write to temp_row the center x,y for sorting in x direction    
        for (y4,x4) in top_row:
            temp_row.append((x4,y4))
        #sort top_row
        top_row = temp_row
        top_row = sorted(top_row)
     
        #sort middle_row
        temp_row=[]
        for (y4,x4) in middle_row:
            temp_row.append((x4,y4))
        middle_row = temp_row
        middle_row = sorted(middle_row)
     
        #sort bottom_row
        temp_row=[]
        for (y4,x4) in bottom_row:
            temp_row.append((x4,y4))
        bottom_row = temp_row
        bottom_row = sorted(bottom_row)
        
        face=[]
        #loop through the 3 positions in each row for the purpose to detecting color of each tile
        for pos in range(3):
            #cut out a 10x10 cube around center of contour
            x,y = top_row[pos]
            cube = resized[int(y)-5:int(y)+5, int(x)-5:int(x)+5]
            hsvcube = cv2.cvtColor(cube, cv2.COLOR_BGR2HSV)
            (h,s,v,tmp) = cv2.mean(hsvcube)
            h = int(round(h))
            s = int(round(s))
            v = int(round(v))
            # ratio of the difference in opencv hsv and image softver hsv values
            hd = 1/360*179 
            sd = 1/100*255 
            vd = 1/100*255 
            if h > 36*hd and h < 60*hd and s > 80*sd and v > 80*vd : 
                face.append("Y")
            elif h > 200*hd and h < 255*hd and s > 60*sd and v > 90*vd :
                face.append("B")    
            elif h > 105*hd and h < 160*hd and s > 60*sd and v > 50*vd :
                face.append("G")
            elif h > 22*hd and h < 37*hd and s > 90*sd and v > 85*vd :
                face.append("O")        
            elif h < 23*hd and s > 75*sd and v > 85*vd :
                face.append("R")
            elif s < 3*sd and v > 90*vd :      
                face.append("W")
            #debugging color detection ranges and contours
            else:
                face.append("X")
            cv2.putText(image, face[pos], (int(x*ratio), int(y*ratio)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        for pos in range(3):
            #cut out a 10x10 cube around center of contour
            x,y = middle_row[pos]
            cube = resized[int(y)-5:int(y)+5, int(x)-5:int(x)+5]
            hsvcube = cv2.cvtColor(cube, cv2.COLOR_BGR2HSV)
            (h,s,v,tmp) = cv2.mean(hsvcube)
            h2 = int(round(h))
            s2 = int(round(s))
            v2 = int(round(v))
            # ratio of the difference in opencv hsv and image softver hsv values
            hd = 1/360*179 
            sd = 1/100*255 
            vd = 1/100*255 
            if h > 36*hd and h < 60*hd and s > 80*sd and v > 80*vd : 
                face.append("Y")
            elif h > 200*hd and h < 255*hd and s > 60*sd and v > 90*vd :
                face.append("B")    
            elif h > 105*hd and h < 160*hd and s > 60*sd and v > 50*vd :
                face.append("G")
            elif h > 22*hd and h < 36*hd and s > 90*sd and v > 85*vd :
                face.append("O")        
            elif h < 23*hd and s > 75*sd and v > 85*vd :
                face.append("R")
            elif s < 3*sd and v > 90*vd :      
                face.append("W")
            #debugging color detection ranges and contours
            else:
                face.append("X")
            cv2.putText(image, face[pos+3], (int(x*ratio), int(y*ratio)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
        for pos in range(3):
            #cut out a 10x10 cube around center of contour
            x,y = bottom_row[pos]
            cube = resized[int(y)-5:int(y)+5, int(x)-5:int(x)+5]
            hsvcube = cv2.cvtColor(cube, cv2.COLOR_BGR2HSV)
            (h,s,v,tmp) = cv2.mean(hsvcube)
            h3 = int(round(h))
            s3 = int(round(s))
            v3 = int(round(v))
            # ratio of the difference in oencv hsv and image softver hsv values
            hd = 1/360*179 
            sd = 1/100*255 
            vd = 1/100*255 
            if h > 36*hd and h < 60*hd and s > 80*sd and v > 80*vd :
                face.append("Y")
            elif h > 200*hd and h < 255*hd and s > 60*sd and v > 90*vd :
                face.append("B")    
            elif h > 105*hd and h < 160*hd and s > 60*sd and v > 50*vd :
                face.append("G")
            elif h > 22*hd and h < 36*hd and s > 90*sd and v > 85*vd :
                face.append("O")        
            elif h < 23*hd and s > 75*sd and v > 85*vd :
                face.append("R")
            elif s < 3*sd and v > 90*vd :      
                face.append("W")
            #debugging color detection ranges and contours
            else:
                face.append("X")
            cv2.putText(image, face[pos+6], (int(x*ratio), int(y*ratio)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
    #if there was 9 colours dectected then check middle tile to know which face to update.
    if len(face) == 9:
        #draw the read colors on the top left of the contour image for debugging
        draw_face(face,65,65,2)
        #based upon which colour the center tile is, update that face for the detected colors and switch the flag of the face that has been read completly
        if face[4] == "W":
            top = face
            top_complete = True
        elif face[4] == "G":
            front = face
            front_complete = True
        elif face[4] == "R":
            right = face
            right_complete = True
        elif face[4] == "O":
            left = face
            left_complete = True
        elif face[4] == "B":
            back = face
            back_complete = True
        elif face[4] == "Y":
            bottom = face
            bottom_complete = True
    
    #draw the read faces each step on a separate image and also on the contour images for debugging
    draw_face(left,0,65,1)
    draw_face(front, 65,65,1)
    draw_face(top,65,0,1)
    draw_face(bottom,65,130,1)
    draw_face(right,130,65,1)
    draw_face(back,195,65,1)
    
    #check to see if all faces have been read
    if top_complete and bottom_complete and front_complete and back_complete and left_complete and right_complete:
        #if all faces read then count up how many of each colour has been detected
        countall = (0,0,0,0,0,0)
        countall = count_colours(top, countall)
        countall = count_colours(bottom, countall)
        countall = count_colours(front,countall)
        countall = count_colours(back, countall)
        countall = count_colours(left, countall)
        countall = count_colours(right, countall)
        (wcount,bcount,rcount,gcount,ycount,ocount)=countall
        #if there are 9 of each color then write result to a text file
        if bcount==9 and rcount==9 and gcount==9 and wcount==9 and ycount==9 and ocount==9:
            cv2.imwrite("net.png", rubik_net)
            cubefile = open('Rubik.txt',"w")   
            cubefile.write("Front (Green side):"+"\n")      
            for ch in front:       
                cubefile.write(ch + " ")     
            cubefile.write("\n\n")     
            cubefile.write("Bottom (Yellow side):"+"\n")      
            for ch in bottom:    
                cubefile.write(ch + " ")     
            cubefile.write("\n\n")      
            cubefile.write("Left (Orange side):"+"\n")     
            for ch in left:       
                cubefile.write(ch + " ")      
            cubefile.write("\n\n")      
            cubefile.write("Right (Red side):"+"\n")
            for ch in right:
                cubefile.write(ch + " ")
            cubefile.write("\n\n")
            cubefile.write("Top (White side):"+"\n")
            for ch in top:
                cubefile.write(ch + " ")
            cubefile.write("\n\n")
            cubefile.write("Back (Blue side):"+"\n")
            for ch in back:
                cubefile.write(ch + " ")
            cubefile.write("\n")
            cubefile.close()
      
      
    #creates the copy of the images with the contours and a step-by-step representation of the net for debugging
    if side == 0:
        cv2.imwrite("1c.png", image)
        #cv2.imwrite("1n.png", rubik_net)
    elif side == 1:
        cv2.imwrite("2c.png", image)
        #cv2.imwrite("2n.png", rubik_net)
    elif side == 2:
        cv2.imwrite("3c.png", image)
        #cv2.imwrite("3n.png", rubik_net)
    elif side == 3:
        cv2.imwrite("4c.png", image)
        #cv2.imwrite("4n.png", rubik_net)
    elif side == 4:
        cv2.imwrite("5c.png", image)
        #cv2.imwrite("5n.png", rubik_net)
    elif side == 5:
        cv2.imwrite("6c.png", image)
        #cv2.imwrite("6n.png", rubik_net)