# MIT License

# Copyright (c) 2016 Akshay Chavan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cv2
import numpy as np
coords = {}

class Rect:

    def __init__(self):
        self.x = None
        self.y = None
        self.w = None
        self.h = None

    def printit(self):
        print (str(self.x) + ',' + str(self.y) + ',' + str(self.w) + ',' + str(self.h))


# endclass

class dragRect:
    def __init__(self):
        # Limits on the canvas
        self.keepWithin = Rect()
        # To store rectangle
        self.outRect = Rect()
        # To store rectangle anchor point
        # Here the rect class object is used to store
        # the distance in the x and y direction from
        # the anchor point to the top-left and the bottom-right corner
        self.anchor = Rect()
        # Selection marker size
        self.sBlk = 4
        # Whether initialized or not
        self.initialized = False

        # Image
        self.image = None

        # Window Name
        self.wname = ""

        # Return flag
        self.returnflag = False

        # FLAGS
        # Rect already present
        self.active = False
        # Drag for rect resize in progress
        self.drag = False
        # Marker flags by positions
        self.TL = False
        self.TM = False
        self.TR = False
        self.LM = False
        self.RM = False
        self.BL = False
        self.BM = False
        self.BR = False
        self.hold = False


# endclass
class utils:
    

    def init(self, dragObj, Img, windowName, windowWidth, windowHeight, initXYWH):
        # Image
        dragObj.image = Img

        # Window name
        dragObj.wname = windowName

        # Limit the selection box to the canvas
        dragObj.keepWithin.x = 0
        dragObj.keepWithin.y = 0
        dragObj.keepWithin.w = windowWidth
        dragObj.keepWithin.h = windowHeight

        # Set rect to zero width and height
        dragObj.outRect.x = initXYWH[0]
        dragObj.outRect.y = initXYWH[1]
        dragObj.outRect.w = initXYWH[2]
        dragObj.outRect.h = initXYWH[3]

        
        

    def initDraw(self, dragObj, Img, windowName, windowWidth, windowHeight, initXYWH):

        self.mouseDown(initXYWH[0], initXYWH[1], dragObj)
        self.mouseMove(initXYWH[0] + initXYWH[2], initXYWH[1] + initXYWH[3], dragObj)
        self.mouseUp(initXYWH[0] + initXYWH[2], initXYWH[1] + initXYWH[3], dragObj)

    # enddef

    def dragrect(self, event, x, y, flags, dragObj):
        if x < dragObj.keepWithin.x:
            x = dragObj.keepWithin.x
        # endif
        if y < dragObj.keepWithin.y:
            y = dragObj.keepWithin.y
        # endif
        if x > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
            x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1
        # endif
        if y > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
            y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1
        # endif

        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseDown(x, y, dragObj)
        # endif
        if event == cv2.EVENT_LBUTTONUP:
            self.mouseUp(x, y, dragObj)
        # endif
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouseMove(x, y, dragObj)
        # endif
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.mouseDoubleClick(x, y, dragObj)
        # endif

    def resultCallBack(self, event, x, y, flags, dragObjs):
        for dragObj in dragObjs:
            if x < dragObj.keepWithin.x:
                x = dragObj.keepWithin.x
            # endif
            if y < dragObj.keepWithin.y:
                y = dragObj.keepWithin.y
            # endif
            if x > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
                x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1
            # endif
            if y > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
                y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1
            # endif

            if event == cv2.EVENT_LBUTTONDOWN:
                if self.mouseDown(x, y, dragObj):
                    break
                    

            # endif
            if event == cv2.EVENT_LBUTTONUP:
                self.mouseUp(x, y, dragObj)

            # endif
            if event == cv2.EVENT_MOUSEMOVE:
                if self.mouseMove(x, y, dragObj):
                    break

            # endif
            if event == cv2.EVENT_LBUTTONDBLCLK:
                self.mouseDoubleClick(x, y, dragObj)
            
    # endif


    def pointInRect(self, pX, pY, rX, rY, rW, rH):
        if rX <= pX <= (rX + rW) and rY <= pY <= (rY + rH):
            return True
        else:
            return False
        # endelseif


    # enddef

    def mouseDoubleClick(self, eX, eY, dragObj):
        if dragObj.active:
            
            if self.pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
                # print ("cur: ", eX, eY, "x, y, w, h: ", dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h)
                dragObj.returnflag = True
                # cv2.destroyWindow(dragObj.wname)
                # cv2.destroyAllWindows()
            # endif

        # endif


    # enddef

    def mouseDown(self, eX, eY, dragObj):
        if dragObj.active:

            if self.pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                        dragObj.outRect.y - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.TL = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                        dragObj.outRect.y - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.TR = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                        dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.BL = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                        dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.BR = True
                return True
            # endif

            if self.pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                        dragObj.outRect.y - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.TM = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                        dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.BM = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                        dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.LM = True
                return True
            # endif
            if self.pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                        dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                        dragObj.sBlk * 2, dragObj.sBlk * 2):
                dragObj.RM = True
                return True
            # endif

            # This has to be below all of the other conditions
            if self.pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
                dragObj.anchor.x = eX - dragObj.outRect.x
                dragObj.anchor.w = dragObj.outRect.w - dragObj.anchor.x
                dragObj.anchor.y = eY - dragObj.outRect.y
                dragObj.anchor.h = dragObj.outRect.h - dragObj.anchor.y
                dragObj.hold = True

                return False

            return False
            # endif

        else:
            dragObj.outRect.x = eX
            dragObj.outRect.y = eY
            dragObj.drag = True
            dragObj.active = True
            return

        # endelseif


    # enddef

    def mouseMove(self, eX, eY, dragObj):

        if dragObj.drag & dragObj.active:
            dragObj.outRect.w = eX - dragObj.outRect.x
            dragObj.outRect.h = eY - dragObj.outRect.y
            self.clearCanvasNDraw(dragObj)
            return True
        # endif

        if dragObj.hold:
            dragObj.outRect.x = eX - dragObj.anchor.x
            dragObj.outRect.y = eY - dragObj.anchor.y

            if dragObj.outRect.x < dragObj.keepWithin.x:
                dragObj.outRect.x = dragObj.keepWithin.x
            # endif
            if dragObj.outRect.y < dragObj.keepWithin.y:
                dragObj.outRect.y = dragObj.keepWithin.y
            # endif
            if (dragObj.outRect.x + dragObj.outRect.w) > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
                dragObj.outRect.x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1 - dragObj.outRect.w
            # endif
            if (dragObj.outRect.y + dragObj.outRect.h) > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
                dragObj.outRect.y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1 - dragObj.outRect.h
            # endif

            self.clearCanvasNDraw(dragObj)
            return True
        # endif

        if dragObj.TL:
            dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
            dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
            dragObj.outRect.x = eX
            dragObj.outRect.y = eY
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.BR:
            dragObj.outRect.w = eX - dragObj.outRect.x
            dragObj.outRect.h = eY - dragObj.outRect.y
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.TR:
            dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
            dragObj.outRect.y = eY
            dragObj.outRect.w = eX - dragObj.outRect.x
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.BL:
            dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
            dragObj.outRect.x = eX
            dragObj.outRect.h = eY - dragObj.outRect.y
            self.clearCanvasNDraw(dragObj)
            return False
        # endif

        if dragObj.TM:
            dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
            dragObj.outRect.y = eY
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.BM:
            dragObj.outRect.h = eY - dragObj.outRect.y
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.LM:
            dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
            dragObj.outRect.x = eX
            self.clearCanvasNDraw(dragObj)
            return False
        # endif
        if dragObj.RM:
            dragObj.outRect.w = eX - dragObj.outRect.x
            self.clearCanvasNDraw(dragObj)
            return False

        return False
        # endif


    # enddef

    def mouseUp(self, eX, eY, dragObj):
        dragObj.drag = False
        self.disableResizeButtons(dragObj)
        self.straightenUpRect(dragObj)
        if dragObj.outRect.w == 0 or dragObj.outRect.h == 0:
            dragObj.active = False
        # endif

        self.clearCanvasNDraw(dragObj)


    # enddef

    def disableResizeButtons(self, dragObj):
        dragObj.TL = dragObj.TM = dragObj.TR = False
        dragObj.LM = dragObj.RM = False
        dragObj.BL = dragObj.BM = dragObj.BR = False
        dragObj.hold = False


    # enddef

    def straightenUpRect(self, dragObj):
        if dragObj.outRect.w < 0:
            dragObj.outRect.x = dragObj.outRect.x + dragObj.outRect.w
            dragObj.outRect.w = -dragObj.outRect.w
        # endif
        if dragObj.outRect.h < 0:
            dragObj.outRect.y = dragObj.outRect.y + dragObj.outRect.h
            dragObj.outRect.h = -dragObj.outRect.h
        # endif


    # enddef

    def clearCanvasNDraw(self, dragObj):
        # Draw
        
        tmp = dragObj.image.copy()
        cv2.rectangle(tmp, (dragObj.outRect.x, dragObj.outRect.y),
                    (dragObj.outRect.x + dragObj.outRect.w,
                    dragObj.outRect.y + dragObj.outRect.h), (0, 255, 0), 2)
        
        self.drawSelectMarkers(tmp, dragObj)
        cv2.imshow(dragObj.wname, tmp)

        global coords

        obj = dragRect()
        obj.outRect.x = dragObj.outRect.x 
        obj.outRect.y = dragObj.outRect.y
        obj.outRect.w = dragObj.outRect.w
        obj.outRect.h = dragObj.outRect.h
        obj.wname = dragObj.wname
        coords[dragObj.wname] = obj

        tmps = []
        
        for key in coords.keys():
            _obj = coords[key]

            tmps.append([_obj.outRect.x, _obj.outRect.y,  _obj.outRect.w, _obj.outRect.h])

            cv2.rectangle(tmp, (_obj.outRect.x, _obj.outRect.y),
                    (_obj.outRect.x + _obj.outRect.w,
                    _obj.outRect.y + _obj.outRect.h), (0, 255, 0), 2)
                    
            self.drawSelectMarkers(tmp, _obj)

        # for outrect in tmps:
        #     print(outrect)
                

    


        # images[dragObj.wname] = tmp
        # tmps = list(images.values())
        # tmps = np.array(tmps, dtype=np.uint8)

        # ret = np.amax(tmps, axis=0)
        # ret = np.array(ret, dtype=np.uint8)

        # print(ret)
        cv2.imshow("result", tmp)



        # key = cv2.waitKey(1)

        # if key == 27:
        #     print(tmps)


    # enddef

    def drawSelectMarkers(self, image, dragObj):
        # Top-Left
        cv2.rectangle(image, (int(dragObj.outRect.x - dragObj.sBlk),
                            int(dragObj.outRect.y - dragObj.sBlk)),
                    (int(dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Top-Rigth
        cv2.rectangle(image, (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk),
                            int(dragObj.outRect.y - dragObj.sBlk)),
                    (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Bottom-Left
        cv2.rectangle(image, (int(dragObj.outRect.x - dragObj.sBlk),
                            int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk)),
                    (int(dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Bottom-Right
        cv2.rectangle(image, (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk),
                            int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk)),
                    (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)

        # Top-Mid
        cv2.rectangle(image, (int(dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk),
                            int(dragObj.outRect.y - dragObj.sBlk)),
                    (int(dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Bottom-Mid
        cv2.rectangle(image, (int(dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk),
                            int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk)),
                    (int(dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Left-Mid
        cv2.rectangle(image, (int(dragObj.outRect.x - dragObj.sBlk),
                            int(dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk)),
                    (int(dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)
        # Right-Mid
        cv2.rectangle(image, (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk),
                            int(dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk)),
                    (int(dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2),
                    int(dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk + dragObj.sBlk * 2)),
                    (0, 255, 0), 2)

    # enddef
