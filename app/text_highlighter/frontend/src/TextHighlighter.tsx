import React, { Component } from 'react'
import Highlightable from "highlightable"
import { Streamlit, StreamlitComponentBase, withStreamlitConnection } from 'streamlit-component-lib';

interface State {
    ranges: any
}

class TextHighlighter extends StreamlitComponentBase<State> {

    render() {
        return (
            <div>
                <Highlightable
                ranges={this.props.args["ranges"]}
                enabled={this.props.args["isEnabled"]}
                onTextHighlighted={
                    (range: any)=> {
                        this.setState({ranges:[range]})
                        console.log("TEXT SELECTED:",range)
                        Streamlit.setComponentValue({"start_idx":range.start, "end_idx":range.end, "text": range.text});
                    }
                }
                highlightStyle={{
                    backgroundColor: '#ffcc80'
                }}
                style={{
                    fontSize : this.props.args["font_size"]
                }}
                text={this.props.args["text"]}
            />
            </div>
        )
    }
}

export default withStreamlitConnection(TextHighlighter);
