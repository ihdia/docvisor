import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from distinctipy import distinctipy

class RegionImage:

    def __init__(self,data,outputMasks):
        self.data = data
        self.path = data["imagePath"]
        self.bbox = data["bbox"]
        self.outputs = data["outputs"]
        self.metrics = data["metrics"]
        self.outputMasks = outputMasks
    
    def processData(self):
        self.image = cv.imread(self.path)

        for output in self.outputs:
            self.outputs[output] = np.array(self.outputs[output])
        
        self.colorMap = {}
        n = len(list(self.outputs.keys()))

        colors = distinctipy.get_colors(n)
        
        c = 0
        for k in self.outputs.keys():
            tempcolor = colors[c]
            self.colorMap[k] = {"polygon":"rgb("+str(tempcolor[0]*255)+","+str(tempcolor[1]*255)+","+str(tempcolor[2]*255)+")",
            "mask":"rgba("+str(tempcolor[0]*255)+","+str(tempcolor[1]*255)+","+str(tempcolor[2]*255)+",0.3)"}
            c += 1


    
    def renderImage(self):
        self.processData()

        x0 = max(int(self.bbox[0]),0)
        y0 = max(int(self.bbox[1]),0)
        w = max(int(self.bbox[2]),0)
        h = max(int(self.bbox[3]),0)

        if x0 - 6 > 0 and y0-2 > 0:
            self.image = self.image[y0-2:y0+h+2,x0-6:x0+w+6]

            # for output in self.outputs:
            #     self.outputs[output][:,0] += 6
            #     self.outputs[output][:,1] += 2
                    
            w += 12
            h += 4

        else:
            self.image = self.image[y0:y0+h,x0:x0+w]
        # else:
        
        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        pil_image = Image.fromarray(self.image)

        self.fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape

        img_width = self.image.shape[1]
        img_height = self.image.shape[0]
        scale_factor = 1
        
        if actual_width/actual_height > 7:
            img_width = 1300
            img_height = 200
            
        elif actual_height/actual_width > 5:
            if actual_width < 200:
                img_width = 200
                img_height = 600
            else:
                img_height = 600
                img_width = 400
            
        else:
            if actual_width < 400 and actual_height < 400:
                img_width = 600
                img_height = actual_height*(600/actual_width)

        for output,pts in self.outputs.items():
            x_zoom = (np.take(pts,0,axis=1) * img_width * scale_factor / actual_width)
            y_zoom = img_height * scale_factor - (np.take(pts,1,axis=1) * img_height * scale_factor / actual_height)

            self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,line_color=self.colorMap[output]["polygon"],name=output+"-polygon",visible='legendonly'))
            self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,name=output+"-pts",visible='legendonly',mode='markers',marker_color=self.colorMap[output]["polygon"]))
            
            if self.outputMasks[output]:
                self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,fill="toself",mode='none',name=output+"-mask",fillcolor=self.colorMap[output]["mask"],visible='legendonly'))

        x_axis_range = img_width * scale_factor
        y_axis_range = img_height * scale_factor

        # Configure axes
        self.fig.update_xaxes(
            visible=False,
            range=[0, x_axis_range]
        )
        
        self.fig.update_yaxes(
            visible=False,
            range=[0, y_axis_range],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x"
        )

        # Add image
        self.fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=pil_image)
        )
        # Configure other layout
        self.fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        self.fig.update_layout(legend=dict(
            orientation="h",
            # xanchor="center",
            yanchor="top",
            y=-0.1, 
            x=0   
        ))

        
        return self.fig

class FullyAutomaticRegionImage:

    def __init__(self,path,data):
        self.path = path
        self.data = data
        self.gtPts = data["groundTruth"]
        self.hasPredPts = True
    
    def processData(self):
        self.image = cv.imread(self.path)

        self.gtPts = np.concatenate((self.gtPts,[self.gtPts[0]]),axis=0)

        if "modelPrediction" in self.data.keys():
            self.predPts = self.data["modelPrediction"]
            self.predPts = np.concatenate((self.predPts,[self.predPts[0]]),axis=0)
        else:
            self.hasPredPts = False
        
    
    def getBbox(self):
        
        if self.hasPredPts:

            minx,miny = np.amin(np.vstack((self.gtPts,self.predPts)),axis=0)
            maxx,maxy = np.amax(np.vstack((self.gtPts,self.predPts)),axis=0)
        
        else:
            minx,miny = np.amin(self.gtPts,axis=0)
            maxx,maxy = np.amax(self.gtPts,axis=0)
        
        minx = max(0,minx-20)
        miny = max(0,miny-20)

        maxx = min(self.image.shape[1],maxx+20)
        maxy = min(self.image.shape[0],maxy+20)
        
        self.bbox = [minx,miny,maxx,maxy]


    def renderImage(self):
        
        self.processData()
        self.getBbox()

        self.gtPts[:,0] -= self.bbox[0]
        self.gtPts[:,1] -= self.bbox[1]

        if self.hasPredPts:
            self.predPts[:,0] -= self.bbox[0]
            self.predPts[:,1] -= self.bbox[1]
        

        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        self.image = self.image[self.bbox[1]:self.bbox[3],self.bbox[0]:self.bbox[2],:]

        pil_image = Image.fromarray(self.image)

        self.fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape

        img_width = self.image.shape[1]
        img_height = self.image.shape[0]
        scale_factor = 1

        if actual_width > 1000:
            if actual_width/actual_height > 10:
                img_width = 1000 
            else:
                img_width = 1000
                img_height = actual_height/(actual_width/1000)
        
        elif actual_height > 700:
            if actual_height/actual_width > 7:
                img_height = 700 
            else:
                img_height = 700
                img_width = actual_width/(actual_height/700)
        
        elif actual_width < 700:
            img_width = 700
            if actual_height < 700:                
                img_height = actual_height*(700/actual_width)
        
        elif actual_height < 700:
            img_height = 700
            if actual_width < 700:
                img_width = actual_width*(700/actual_height)

        x_gt_zoom = (np.take(self.gtPts,0,axis=1) * img_width * scale_factor / actual_width)
        y_gt_zoom = img_height * scale_factor - (np.take(self.gtPts,1,axis=1) * img_height * scale_factor / actual_height)

        self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,line_color='blue',name="ground truth polygon",visible='legendonly'))
        self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,name="ground truth points",visible='legendonly',mode='markers',marker_color='rgb(0,180,255)'))    
        
        if self.hasPredPts != False:
        
            x_model_zoom = np.take(self.predPts,0,axis=1) * img_width * scale_factor / actual_width
            y_model_zoom = img_height * scale_factor - (np.take(self.predPts,1,axis=1) * img_height * scale_factor / actual_height)

            self.fig.add_trace(go.Scatter(x= x_model_zoom,y=y_model_zoom,line_color='green',name='model predicted polygon',visible='legendonly'))        

        x_axis_range = img_width * scale_factor
        y_axis_range = img_height * scale_factor

        # Configure axes
        self.fig.update_xaxes(
            visible=False,
            range=[0, x_axis_range]
        )
        
        self.fig.update_yaxes(
            visible=False,
            range=[0, y_axis_range],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x"
        )

        # Add image
        self.fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=pil_image)
        )
        # Configure other layout
        self.fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        self.fig.update_layout(legend=dict(
            orientation="h",
            # xanchor="center",
            yanchor="top",
            y=-0.1, 
            x=0   
        ))

        
        return self.fig

class FullDocumentImage:

    def __init__(self,data,regionShown=None):
        self.data = data
        self.path = data["imagePath"]
        self.regionShown = regionShown
    
    def processData(self):
        self.image = cv.imread(self.path)
    
    def renderImage(self):
        self.processData()

        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        pil_image = Image.fromarray(self.image)

        fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape

        img_height = min(max(self.image.shape[0],500),600)
        img_width = min(max(self.image.shape[1]/1.5,1000),1500)

        scale_factor = 1

        firstRegion = 0

        for region in self.data["regions"]:

            gtPts = np.array(region["groundTruth"])
            gtPts = np.concatenate((gtPts,[gtPts[0]]),axis=0)

            xGtZoom = (np.take(gtPts,0,axis=1) * img_width * scale_factor / actual_width)
            yGtZoom = img_height * scale_factor - (np.take(gtPts,1,axis=1) * img_height * scale_factor / actual_height)

            fig.add_trace(go.Scatter(x = xGtZoom,y = yGtZoom,line_color='blue',name="ground truth polygons",visible='legendonly',legendgroup='1',showlegend=(region==self.data["regions"][0])))
            fig.add_trace(go.Scatter(x = xGtZoom,y = yGtZoom,name="ground truth points",visible='legendonly',mode='markers',marker_color='rgb(0,180,255)',legendgroup='2',showlegend=(region==self.data["regions"][0])))    
            
            if "modelPrediction" in region.keys():

                if firstRegion == 0:
                    firstRegion = region

                predPts = np.array(region["modelPrediction"])
                predPts = np.concatenate((predPts,[predPts[0]]),axis=0)

                xPredZoom = np.take(predPts,0,axis=1) * img_width * scale_factor / actual_width
                yPredZoom = img_height * scale_factor - (np.take(predPts,1,axis=1) * img_height * scale_factor / actual_height)

                fig.add_trace(go.Scatter(x= xPredZoom,y=yPredZoom,line_color='green',name='model predicted polygons',visible='legendonly',legendgroup='3',showlegend=(region==firstRegion)))
            

        if self.regionShown is not None:
        
            regionShownPts = self.regionShown["groundTruth"]

            xZoom = (np.take(regionShownPts,0,axis=1) * img_width * scale_factor / actual_width)
            yZoom = img_height * scale_factor - (np.take(regionShownPts,1,axis=1) * img_height * scale_factor / actual_height)

            fig.add_trace(go.Scatter(x = xZoom,y = yZoom,fill="toself",mode='none',name="region shown",fillcolor='rgba(255,0,0,0.3)'))
        
        xAxisRange = img_width * scale_factor
        yAxisRange = img_height * scale_factor

        # Configure axes
        fig.update_xaxes(
            visible=False,
            range=[0, xAxisRange]
        )
        
        fig.update_yaxes(
            visible=False,
            range=[0, yAxisRange],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x"
        )

        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=pil_image)
        )
        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        fig.update_layout(legend=dict(
            orientation="h",
            xanchor="left",
            yanchor="top",
            y=-0.1, 
            x=0   
        ))
        
        return fig        
