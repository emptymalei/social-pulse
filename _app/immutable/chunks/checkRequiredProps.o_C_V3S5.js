function n(e){if(e===null||typeof e!="object")throw Error("reqProps must be a non-null object");if(Object.keys(e).length===0)throw Error("reqProps must not be empty");const r=[];for(const[o,t]of Object.entries(e))t===void 0&&r.push(`Missing required prop: "${o}".`);if(r.length>0)throw new Error(r.join(`
`))}export{n as c};
