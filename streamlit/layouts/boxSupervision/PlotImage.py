import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from distinctipy import distinctipy

class RegionImage:

    def __init__(self,data,outputMasks,outputs_locked):
        self.data = data
        self.path = data["imagePath"]
        self.bbox = data["bbox"]
        self.outputs = data["outputs"]
        self.outputMasks = outputMasks
        self.outputsLocked = outputs_locked
    
    def processData(self):
        self.image = cv.imread(self.path)

        for output in self.outputs:
            self.outputs[output] = np.concatenate((np.array(self.outputs[output]),[self.outputs[output][0]]),axis=0)
        
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
                    
            w += 12
            h += 4

        else:
            self.image = self.image[y0:y0+h,x0:x0+w]
        
        self.image = cv.cvtColor(self.image,cv.COLOR_RGB2BGR)
        pil_image = Image.fromarray(self.image)

        self.fig = go.Figure()
        actual_height, actual_width, _ = self.image.shape

        img_width = self.image.shape[1]
        img_height = self.image.shape[0]
        scale_factor = 1
        
        if actual_width/actual_height > 7:
            img_width = 1500
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

            if self.outputsLocked[output+"-polygon"]:
                self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,line_color=self.colorMap[output]["polygon"],name=output+"-polygon"))
            else:    
                self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,line_color=self.colorMap[output]["polygon"],name=output+"-polygon",visible='legendonly'))
            
            if self.outputsLocked[output+"-pts"]:
                self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,name=output+"-pts",mode='markers',marker_color=self.colorMap[output]["polygon"]))    
            else:
                self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,name=output+"-pts",visible='legendonly',mode='markers',marker_color=self.colorMap[output]["polygon"]))
            
            if self.outputMasks[output]:
                if self.outputsLocked[output+"-mask"]:
                    self.fig.add_trace(go.Scatter(x = x_zoom,y = y_zoom,fill="toself",mode='none',name=output+"-mask",fillcolor=self.colorMap[output]["mask"]))
                else:
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
            # xanchor="right",
            yanchor="bottom",
            y=-0.1, 
            x=0   
        ))

        
        return self.fig
