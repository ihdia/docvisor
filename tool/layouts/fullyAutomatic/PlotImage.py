import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from distinctipy import distinctipy

class FullyAutomaticRegionImage:

    def __init__(self,path,data,outputs_locked,outputMasks):
        self.path = path
        self.data = data
        self.gtPts = data["groundTruth"]
        self.hasPredPts = True
        self.outputsLocked = outputs_locked
        self.outputMasks = outputMasks
    
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
        
        self.bbox = [int(minx),int(miny),int(maxx),int(maxy)]


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
        
        elif actual_height > 400:            
            if actual_height/actual_width > 7:
                img_height = 400 
            else:
                img_height = 400
                img_width = actual_width/(actual_height/400)

        elif actual_height < 350:
            img_height = 350
            if actual_width < 350:
                img_width = actual_width*(350/actual_height)

        # elif actual_width < 1000:            
        #     img_width = actual_width
        #     if actual_height < 1000:                
        #         img_height = actual_height*(1000/actual_width) + 100
        

        x_gt_zoom = (np.take(self.gtPts,0,axis=1) * img_width * scale_factor / actual_width)
        y_gt_zoom = img_height * scale_factor - (np.take(self.gtPts,1,axis=1) * img_height * scale_factor / actual_height)

        
        if self.outputsLocked["groundTruth-polygon"]:
            self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,line_color='blue',name="groundTruth-polygon"))
        else:
            self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,line_color='blue',name="groundTruth-polygon",visible='legendonly'))
        
        if self.outputsLocked["groundTruth-pts"]:
            self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,name="groundTruth-pts",mode='markers',marker_color='rgb(0,180,255)'))    
        else:
            self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,name="groundTruth-pts",visible='legendonly',mode='markers',marker_color='rgb(0,0,255)'))    
        
        if self.outputMasks["groundTruth"]:
            if self.outputsLocked["groundTruth-mask"]:
                self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,fill="toself",mode='none',name="groundTruth-mask",fillcolor='rgba(0,0,255,0.3)'))
            else:
                self.fig.add_trace(go.Scatter(x = x_gt_zoom,y = y_gt_zoom,fill="toself",mode='none',name="groundTruth-mask",fillcolor='rgba(0,0,255,0.3)',visible='legendonly'))

        
        
        if self.hasPredPts != False:
        
            x_model_zoom = np.take(self.predPts,0,axis=1) * img_width * scale_factor / actual_width
            y_model_zoom = img_height * scale_factor - (np.take(self.predPts,1,axis=1) * img_height * scale_factor / actual_height)

            if self.outputsLocked["modelPrediction-polygon"]:
                self.fig.add_trace(go.Scatter(x= x_model_zoom,y=y_model_zoom,line_color='green',name='modelPrediction-polygon'))        
            else:
                self.fig.add_trace(go.Scatter(x= x_model_zoom,y=y_model_zoom,line_color='green',name='modelPrediction-polygon',visible='legendonly'))       

            if self.outputMasks["modelPrediction"]:
                if self.outputsLocked["modelPrediction-mask"]:
                    self.fig.add_trace(go.Scatter(x = x_model_zoom,y = y_model_zoom,fill="toself",mode='none',name="modelPrediction-mask",fillcolor='rgba(0,255,0,0.3)'))
                else:
                    self.fig.add_trace(go.Scatter(x = x_model_zoom,y = y_model_zoom,fill="toself",mode='none',name="modelPrediction-mask",fillcolor='rgba(0,255,0,0.3)',visible='legendonly'))

            


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
            # xanchor="right",
            yanchor="bottom",
            y=-0.1, 
            x=0   
        ))

        
        return self.fig

class FullDocumentImage:

    def __init__(self,data,outputs_locked,outputMasks,regionShown=None):
        self.data = data
        self.path = data["imagePath"]
        self.regionShown = regionShown
        self.outputsLocked = outputs_locked
        self.outputMasks = outputMasks
    
    def processData(self):
        self.image = cv.imread(self.path)
    
    def renderImage(self):
        self.processData()

        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        pil_image = Image.fromarray(self.image)

        fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape

        
        img_width = min(max(self.image.shape[1]/1.5,1000),1500)

        if actual_height > 800:
            img_height = min(max(self.image.shape[0],800),900)
        else:
            img_height = min(max(self.image.shape[0],500),600)

        # img_width = actual_width
        # img_height = actual_height

        # print(img_height/actual_height)
        # print(img_width/actual_width)

        scale_factor = 1

        firstRegion = 0

        for region in self.data["regions"]:

            gtPts = np.array(region["groundTruth"])
            gtPts = np.concatenate((gtPts,[gtPts[0]]),axis=0)

            xGtZoom = (np.take(gtPts,0,axis=1) * img_width * scale_factor / actual_width)
            yGtZoom = img_height * scale_factor - (np.take(gtPts,1,axis=1) * img_height * scale_factor / actual_height)

            if self.outputsLocked["groundTruth-polygons"]:
                fig.add_trace(go.Scattergl(x = xGtZoom,y = yGtZoom,line_color='blue',name="groundTruth-polygons",legendgroup='1',showlegend=(region==self.data["regions"][0])))
            else:
                fig.add_trace(go.Scattergl(x = xGtZoom,y = yGtZoom,line_color='blue',name="groundTruth-polygons",visible='legendonly',legendgroup='1',showlegend=(region==self.data["regions"][0])))
            
            if self.outputsLocked["groundTruth-pts"]:
                fig.add_trace(go.Scattergl(x = xGtZoom,y = yGtZoom,name="groundTruth-pts",mode='markers',marker_color='rgb(0,0,255)',legendgroup='2',showlegend=(region==self.data["regions"][0])))    
            else:
                fig.add_trace(go.Scattergl(x = xGtZoom,y = yGtZoom,name="groundTruth-pts",visible='legendonly',mode='markers',marker_color='rgb(0,0,255)',legendgroup='2',showlegend=(region==self.data["regions"][0])))    
            
            if self.outputMasks["groundTruth"]:
                if self.outputsLocked["groundTruth-mask"]:
                    fig.add_trace(go.Scatter(x = xGtZoom,y = yGtZoom,fill="toself",mode='none',name="groundTruth-mask",fillcolor='rgba(0,0,255,0.3)',legendgroup='3',showlegend=(region==self.data["regions"][0])))    
                else:
                    fig.add_trace(go.Scatter(x = xGtZoom,y = yGtZoom,fill="toself",mode='none',name="groundTruth-mask",fillcolor='rgba(0,0,255,0.3)',visible='legendonly',legendgroup='3',showlegend=(region==self.data["regions"][0])))    
            
            if "modelPrediction" in region.keys():

                if firstRegion == 0:
                    firstRegion = region

                predPts = np.array(region["modelPrediction"])
                predPts = np.concatenate((predPts,[predPts[0]]),axis=0)

                xPredZoom = np.take(predPts,0,axis=1) * img_width * scale_factor / actual_width
                yPredZoom = img_height * scale_factor - (np.take(predPts,1,axis=1) * img_height * scale_factor / actual_height)

                if self.outputsLocked["modelPrediction-polygons"]:
                    fig.add_trace(go.Scattergl(x= xPredZoom,y=yPredZoom,line_color='green',name='modelPrediction-polygons',legendgroup='4',showlegend=(region==firstRegion)))
                else:
                    fig.add_trace(go.Scattergl(x= xPredZoom,y=yPredZoom,line_color='green',name='modelPrediction-polygons',visible='legendonly',legendgroup='4',showlegend=(region==firstRegion)))
                
                if self.outputMasks["modelPrediction"]:
                    if self.outputsLocked["modelPrediction-mask"]:
                        fig.add_trace(go.Scatter(x = xPredZoom,y = yPredZoom,fill="toself",mode='none',name="modelPrediction-mask",fillcolor='rgba(0,255,0,0.3)',legendgroup='5',showlegend=(region==self.data["regions"][0])))    
                    else:
                        fig.add_trace(go.Scatter(x = xPredZoom,y = yPredZoom,fill="toself",mode='none',name="modelPrediction-mask",fillcolor='rgba(0,255,0,0.3)',visible='legendonly',legendgroup='5',showlegend=(region==self.data["regions"][0])))    
                


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
            # xanchor="right",
            yanchor="bottom",
            y=-0.1, 
            x=0   
        ))
        
        return fig
