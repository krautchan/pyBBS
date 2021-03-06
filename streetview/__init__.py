'''
Created on Jul 23, 2012

@author: teddydestodes
'''
import os
import requests
import json
from urllib import urlretrieve
from math import fabs
import Image


class Streetview(object):
    
    def __init__(self, datadir='/var/lib/streetview/', width=1280, height=800, panoid='mNv59_lFPBsk78x9t1RYhw'):
        self.datadir = datadir
        self.width = width
        self.height = height
        self.panoid = panoid
        self.zoomlevel = 3
        self.getPanoInfo(self.panoid)
        self.getPanoImages(self.panoid)
    
    def decode_line(self,encoded):
        """Decodes a polyline that was encoded using the Google Maps method.
    
        See http://code.google.com/apis/maps/documentation/polylinealgorithm.html
        
        This is a straightforward Python port of Mark McClure's JavaScript polyline decoder
        (http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/decode.js)
        and Peter Chng's PHP polyline decode
        (http://unitstep.net/blog/2008/08/02/decoding-google-maps-encoded-polylines-using-php/)
        """
        encoded_len = len(encoded)
        index = 0
        array = []
        lat = 0
        lng = 0
        while index < encoded_len:
            b = 0
            shift = 0
            result = 0
            while True:
                b = ord(encoded[index]) - 63
                index = index + 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            dlat = ~(result >> 1) if result & 1 else result >> 1
            lat += dlat
            shift = 0
            result = 0
            while True:
                b = ord(encoded[index]) - 63
                index = index + 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            dlng = ~(result >> 1) if result & 1 else result >> 1
            lng += dlng
            array.append((lat * 1e-5, lng * 1e-5))
        return array
    
    def getYaw(self):
        return self.getPanoInfo(self.panoid)['Projection']['pano_yaw_deg']
    
    def getLinks(self):
        return self.getPanoInfo(self.panoid)['Links']
    
    def setPanoId(self,panoid):
        self.panoid = panoid
        self.getPanoInfo(self.panoid)
        self.getPanoImages(self.panoid)
    
    def getPanoInfo(self, panoid):
        data = None
        if not os.path.exists(os.path.join(self.datadir,panoid)):
            os.makedirs(os.path.join(self.datadir,panoid))
        if not os.path.exists(os.path.join(self.datadir,panoid,'data.json')):
            url = 'http://cbk0.googleapis.com/cbk?output=json&oe=utf-8&panoid=%s&v=0' % panoid
            r = requests.get(url)
            data = json.loads(r.content)
            f = open(os.path.join(self.datadir,panoid,'data.json'), 'w')
            json.dump(data,f)
            f.close()
        else:
            f = open(os.path.join(self.datadir,panoid,'data.json'), 'r')
            data = json.load(f)
            f.close()
        return data
    
    def getPanoImages(self,panoid):
        for x in range(0,8):
            for y in range(0,4):
                filename = '%02d-%02d.jpg' % (x,y)
                if not os.path.exists(os.path.join(self.datadir,panoid)):
                    os.makedirs(os.path.join(self.datadir,panoid))
                url = 'http://cbk1.googleapis.com/cbk?output=tile&cb_client=apiv3&v=4&zoom=%d&x=%d&y=%d&panoid=%s' % (self.zoomlevel,x,y,panoid)
                outpath = os.path.join(self.datadir,panoid,filename)
                if not os.path.exists(outpath):
                    urlretrieve(url, outpath)
                    
    def makeViewport(self,yaw=0, pitch=0):
        camcenter = (1664,832,3328,832)
        f = open(os.path.join(self.datadir,self.panoid,'data.json'), 'r')
        data = json.load(f)
        f.close()
        #print data
        height = int(data['Data']['image_height'])/(self.zoomlevel+1)
        width = int(data['Data']['image_width'])/(self.zoomlevel+1)
        tile_width = int(data['Data']['tile_width'])
        tile_height = int(data['Data']['tile_height'])
        yawoffset = float(data['Projection']['pano_yaw_deg'])
        yaw = yawoffset + yaw
        import math
        b = math.pi/180
        
        s = width/360
        xcenter = s*yaw
        while xcenter < 0:
            xcenter += width
        while xcenter > width:
            xcenter -= width
        pitch += 90
        s = height/180
        ycenter = s*pitch
        while ycenter < 0:
            ycenter += height
        while ycenter > height:
            ycenter -= height
        xstart = (xcenter-self.width/2)
        xend   = (xcenter+self.width/2)+tile_width
        ystart = (ycenter-self.height/2)
        yend   = (ycenter+self.height/2)
        
        xtiles = int(math.ceil(width/tile_width))
        ytiles = int(math.ceil(height/tile_height))
        offset = (int(xcenter-self.width/2),int(ycenter-self.height/2))
        view = Image.new('RGBA', (self.width,self.height))
        for x in range(offset[0] / 512,((offset[0]+self.width)/512)+1):
            if x < 0:
                xoff = (x*512)-offset[0]+256
                x = xtiles
            else:
                xoff = (x*512)-offset[0]
            for y in range(offset[1] / 512,((offset[1]+self.height)/512)+1):
                yoff = (y*512)-offset[1]
                filename = os.path.join(self.datadir,self.panoid,'%02d-%02d.jpg' % (x,y))
                img = Image.open(filename)
                toffset = (xoff,yoff)
                view.paste(img,toffset)
            if x >= xtiles:
                x = x-xtiles
                xoff = (x*512)-offset[0]+256
                for y in range(offset[1] / 512,((offset[1]+self.height)/512)+1):
                    yoff = (y*512)-offset[1]
                    filename = os.path.join(self.datadir,self.panoid,'%02d-%02d.jpg' % (x,y))
                    img = Image.open(filename)
                    toffset = (xoff,yoff)
                    view.paste(img,toffset)
        #self.drawRect(view, (int(xcenter),int(ycenter)))
        return view
    
    def drawRect(self, image, pos):
        for x in range(-10,10):
            for y in range(-10,10):
                if pos[0]+x>0 and pos[1]+y>0 and pos[0]+x < image.size[0] and pos[1]+y < image.size[1]:
                    image.putpixel((pos[0]+x, pos[1]+y),(255,0,0,0))