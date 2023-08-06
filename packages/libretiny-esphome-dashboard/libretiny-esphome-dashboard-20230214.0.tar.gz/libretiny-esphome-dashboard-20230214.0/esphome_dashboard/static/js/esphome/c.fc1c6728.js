import{r as o,b as t,d as e,l as i,n as r,s,y as a,Q as n}from"./index-f2af38a5.js";import"./c.13f7e761.js";import{o as c}from"./c.30a0677d.js";import"./c.419250e6.js";import"./c.63fcbfd6.js";import"./c.33591792.js";import"./c.32c39114.js";import"./c.f7445c67.js";let d=class extends s{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${n(this.configuration,this.downloadFactoryFirmware)}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const t=document.createElement("a");t.download=this.configuration+".bin",t.href=n(this.configuration,this.downloadFactoryFirmware),document.body.appendChild(t),t.click(),t.remove()}_handleRetry(){c(this.configuration,this.downloadFactoryFirmware)}_handleClose(){this.parentNode.removeChild(this)}};d.styles=o`
    a {
      text-decoration: none;
    }
  `,t([e()],d.prototype,"configuration",void 0),t([e()],d.prototype,"downloadFactoryFirmware",void 0),t([i()],d.prototype,"_result",void 0),d=t([r("esphome-compile-dialog")],d);
