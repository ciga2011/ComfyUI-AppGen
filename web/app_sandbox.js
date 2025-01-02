import { app } from '../../../scripts/app.js'
import { api } from "../../../scripts/api.js";
import { $el } from "../../../scripts/ui.js";

const _ID = 'AG_APP_SANDBOX'

app.registerExtension({
  name: "AppGen." + _ID,
  async beforeRegisterNodeDef(nodeType, nodeData, app){
    
    if(nodeData.name !== _ID) return
    
    console.log('Load AppGen Sandbox...', nodeType, nodeData, app)
    
    let elIFrame = null
        
    const onNodeCreated = nodeType.prototype.onNodeCreated
    nodeType.prototype.onNodeCreated = async function(){
      const r = onNodeCreated 
        ? onNodeCreated.apply(this, arguments)
        : undefined
      
      //console.log('==>', this, this.widgets[0])
      //console.log('widgets=>', app.widgets)
      
      const e = $el("div.sandbox", {}, [
        $el('iframe', {
          style: { width: '100%', height: '100%', border: 0},
          srcdoc: ''
        })
      ])
      //console.log('e =>', e)
      const w = this.addDOMWidget("test", "test", e)
      w.computeSize = () => {
        return [this.size[0], 200]
      }            
      
      const origDraw = w.draw
      w.draw = function(){
        origDraw.apply(this, arguments)
        //console.log('draw arguments =>', arguments)
        const [ctx, node, w, y] = arguments
        e.style.height = (node.size[1] - 50) + 'px'
      }
              
      elIFrame = e.querySelector('iframe')
      
      return r  
    }
    
    const onExecuted = nodeType.prototype.onExecuted
    nodeType.prototype.onExecuted = async function(message){
      onExecuted?.apply(this, arguments);
      console.log('onExecuted =>', message)
      if(elIFrame){
        elIFrame.srcdoc = message.text.join('')
      }
    }
    
  }
})