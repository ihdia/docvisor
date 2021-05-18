import {Streamlit, StreamlitComponentBase, withStreamlitConnection,} from "streamlit-component-lib"
import React from "react"
import ReactCrop from 'react-image-crop'
import 'react-image-crop/dist/ReactCrop.css'

interface State {
	crop: any
	imgRef: any
}

class ROISelector extends StreamlitComponentBase<State> {
	constructor(props: any) {
        super(props);

        this.state = {
			crop: {
				unit: "%"
				// default crop width and height you can comment two for manual crop
				// width: 100,
			},
			imgRef : React.createRef()
        };
    }

	onChange = (_: any,percentCrop: any) => {
		// console.log("onChange")
		if("height" in this.state.crop){
				percentCrop.height = 100;
				percentCrop.y = 0;
		}
		this.setState({...this.state, crop: percentCrop });

	  };


	onComplete = (newCrop: any) => {
			// console.log("onComplete")
			if (newCrop.width) {
				let img = this.state.imgRef.current;
				let scaleX = img.naturalWidth/ img.width;
				
				let finalCrop = {"start_px": Math.round(newCrop.x * scaleX), "end_px": Math.round((newCrop.x + newCrop.width)*scaleX), "key":this.props.args["key"]};
				console.log("CROPPED ROI:", finalCrop, !this.props.args["isEnabled"]);
				Streamlit.setComponentValue(finalCrop)
			}
	};

	 onImageLoaded = (img: any)=> {
	 	 // console.log("onImageLoaded")
		 this.state.imgRef.current = img
	 };

	render() {

		return (
			<div>
			<ReactCrop src={this.props.args["img_b64"]} crop={this.state.crop}
						disabled={!this.props.args["isEnabled"]}
					   	onImageLoaded={this.onImageLoaded}
						onChange={this.onChange}
						onComplete={this.onComplete}
						/>
			</div>
		)
	}
}

export default withStreamlitConnection(ROISelector)
