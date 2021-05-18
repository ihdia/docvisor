import { Streamlit, RenderData } from "streamlit-component-lib"

const span = document.body.appendChild(document.createElement("span"))

const pred_text = span.appendChild(document.createTextNode(""))



// const button = span.appendChild(document.createElement("button"))

let out_data = {'start':-1,'end':-1}

span.addEventListener('mouseup',function(e)
{
  var selection = window.getSelection();
  let start = selection?.anchorOffset;
  let end = selection?.focusOffset;
  out_data['start'] = start==null?-1:start;
  out_data['end'] = end==null?-1:end;
  Streamlit.setComponentValue(out_data);
})


// button.textContent = "Highlight Me!"

// Add a click handler to our button. It will send data back to Streamlit.
// let numClicks = 0
let isFocused = false
// button.onclick = function(): void {
//   // Increment numClicks, and pass the new value back to
//   // Streamlit via `Streamlit.setComponentValue`.
//   // numClicks += 1
//   console.log(out_data);
//   Streamlit.setComponentValue(out_data);

// }
//
// button.onfocus = function(): void {
//   isFocused = true
// }
// //
// button.onblur = function(): void {
//   isFocused = false
// }

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  // Maintain compatibility with older versions of Streamlit that don't send
  // a theme object.
  if (data.theme) {
    // Use CSS vars to style our button border. Alternatively, the theme style
    // is defined in the data.theme object.
    const borderStyling = `1px solid var(${
      isFocused ? "--primary-color" : "gray"
    })`
    // button.style.border = borderStyling
    // button.style.outline = borderStyling
  }

  // Disable our button if necessary.
  // button.disabled = data.disabled

  // RenderData.args is the JSON dictionary of arguments sent from the
  // Python script.
  let pred = data.args["pred"]
  let ground = data.args["ground"]

  // Show "Hello, name!" with a non-breaking space afterwards.
  // textNode.textContent = `Hello, ${name}! ` + String.fromCharCode(160)
  pred_text.textContent = pred
  span.style.fontSize = "30px";
  // ground_text.textContent = ground

  // We tell Streamlit to update our frameHeight after each render event, in
  // case it has changed. (This isn't strictly necessary for the example
  // because our height stays fixed, but this is a low-cost function, so
  // there's no harm in doing it redundantly.)
  Streamlit.setFrameHeight()
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
