/* ERCOT Research Connections — a read-only research graph browser.
   The graph's directional labels and editorial weights are preserved.
   Curves indicate documented links, NOT statistical relationships or causality. */
"use strict";
const conn={filter:"all",limit:10,selected:null,mode:"map",trail:[],target:"SRC-PRED",observer:null};
const CONN_GROUPS=[
 ["finding","Findings","#77c7d9"],["model","Models","#82b9e4"],["metric","Metrics","#6dc8ad"],
 ["visual","Figures","#9a96e7"],["limitation","Caveats","#e4ae7a"],
 ["source","Sources & data","#7c9ec9"],["question","Questions & context","#c8a0c7"]
];
const CONN_FILTERS=["all","finding","model","metric","visual","limitation","source","question"];
function connGroup(n){if(!n)return"question";if(n.type==="finding")return"finding";if(n.type==="model")return"model";if(n.type==="metric")return"metric";if(n.type==="visual"||n.type==="visual_collection")return"visual";if(n.type==="limitation"||n.type==="open")return"limitation";if(n.type==="source"||n.type==="data")return"source";return"question";}
function connGroupName(g){return CONN_GROUPS.find(x=>x[0]===g)?.[1]||"Related context";}
function connColor(g){return CONN_GROUPS.find(x=>x[0]===g)?.[2]||"#a9c2da";}
function connLinks(id){const m=new Map();for(const e of state.adj.get(id)||[]){
 const other=e.from===id?e.to:e.from,n=node(other);if(!n)continue;
 if(!m.has(other))m.set(other,{id:other,n,group:connGroup(n),edges:[]});
 m.get(other).edges.push(e);
 }
 return [...m.values()].map(o=>{o.edges.sort((a,b)=>b.weight-a.weight||a.relation.localeCompare(b.relation));o.primary=o.edges.find(e=>e.kind!=="presentation")||o.edges[0];o.weight=o.primary.weight;return o;})
 .sort((a,b)=>b.weight-a.weight||a.n.title.localeCompare(b.n.title));
}
function connBalanced(rows,limit){const buckets=new Map();for(const c of rows){if(!buckets.has(c.group))buckets.set(c.group,[]);buckets.get(c.group).push(c);}
 const rank=CONN_GROUPS.map(x=>x[0]),out=[];while(out.length<limit){let any=false;
  for(const key of rank){const arr=buckets.get(key);if(arr&&arr.length){out.push(arr.shift());any=true;if(out.length>=limit)break;}}
  if(!any)break;
 }return out;}
function connGo(id){if(!node(id))return;const prev=state.graphFocus;
 state.graphFocus=id;conn.selected=null;conn.limit=10;conn.mode="map";
 if(!conn.trail.length)conn.trail=[prev];if(conn.trail.at(-1)!==id)conn.trail.push(id);if(conn.trail.length>8)conn.trail.shift();
 history.pushState(null,"","#graph="+encodeURIComponent(id));render();document.getElementById("cx-focus-picker")?.focus();}
function connStepBack(){if(conn.trail.length<2)return;conn.trail.pop();const id=conn.trail.at(-1);state.graphFocus=id;conn.selected=null;conn.limit=10;history.pushState(null,"","#graph="+encodeURIComponent(id));render();}
function connReset(){conn.trail=[];conn.filter="all";conn.limit=10;conn.selected=null;connGo("FIND-OVERALL");}
function connOptions(selected,changed,aria){const pick=make("select","cx-select");pick.setAttribute("aria-label",aria);const groups=[["Findings","finding"],["Notebook figures","visual"],["Models","model"],["Numeric evidence","metric"],["Limitations","limitation"],["Sources and data","source"],["Questions, methods and context","other"]];const accounted=new Set(groups.slice(0,-1).map(x=>x[1]));
 groups.forEach(([label,type])=>{const grp=make("optgroup");grp.label=label;const candidates=type==="other"?state.graph.nodes.filter(n=>!accounted.has(n.type)):state.graph.nodes.filter(n=>n.type===type);
 candidates.sort((a,b)=>a.title.localeCompare(b.title)).forEach(n=>{const option=make("option","",n.title);option.value=n.id;put(grp,option);});if(grp.children.length)put(pick,grp);});
 pick.value=selected;pick.addEventListener("change",()=>changed(pick.value));return pick;}
function connMetaLine(parent,text){put(parent,make("span","cx-small",text));}
function connGraphHeading(root){const intro=sectionTitle("RESEARCH / CONNECTIONS","Explore how the research fits together","Choose a finding or figure, then follow the lines to its numerical evidence, questions, data sources and limitations. Each link has a recorded reason.");put(root,intro);}
function connSummary(links){const counts=new Map();for(const c of links)counts.set(c.group,(counts.get(c.group)||0)+1);return counts;}
function connFacetBar(root,links){const bar=make("div","cx-facets"),counts=connSummary(links);
 const names=[["all","All connections"],...CONN_GROUPS.map(g=>[g[0],g[1]])];
 names.forEach(([id,label])=>{const count=id==="all"?links.length:counts.get(id)||0;if(!count&&id!=="all")return;
  const b=clickable(label+" · "+count,()=>{conn.filter=id;conn.limit=10;conn.selected=null;render();},"cx-facet"+(conn.filter===id?" active":""));b.setAttribute("aria-pressed",String(conn.filter===id));put(bar,b);});
 put(root,bar);}
function connRelationshipLabel(edge,id){if(edge.flow!=="dependency")return "Documented association (not causal)";
 return edge.from===id?"Related concept depends on the selected concept":"Selected concept depends on the related concept";}
function connMainCard(focus,links){const card=make("div","cx-hub");card.id="cx-hub";put(card,make("div","cx-hub-eyebrow","SELECTED "+readable(focus.type)),make("h2","",focus.title),make("p","",truncate(focus.summary,215)));
 const actions=make("div","cx-hub-actions");put(actions,clickable("Inspect record",()=>openNode(focus.id),"cx-btn"),clickable("Copy ID",()=>copyText(focus.id),"cx-btn subtle"));put(card,actions,make("div","cx-hub-stats",links.length+" unique linked concepts · "+focus.id));return card;}
function connNeighborCard(link,focusId){const card=make("div","cx-node"+(conn.selected===link.id?" is-selected":""));card.dataset.nodeId=link.id;card.style.setProperty("--node-color",connColor(link.group));
 const top=make("div","cx-node-header");put(top,make("span","cx-node-kind",connGroupName(link.group)),make("span","cx-node-direction",link.primary.flow==="dependency"?(link.primary.to===focusId?"→ selected":"selected →"):"↔"));put(card,top,make("h3","",link.n.title),make("p","cx-relationship",link.primary.relation));
 const controls=make("div","cx-node-actions");const why=clickable("Why linked?",()=>{conn.selected=link.id;render();document.getElementById("cx-explanation")?.scrollIntoView({block:"nearest",behavior:"smooth"});},"cx-why"),follow=clickable("Follow →",()=>connGo(link.id),"cx-follow");put(controls,why,follow);put(card,controls);return card;}
function connDiagram(root,focus,all,filtered,shown){const section=make("section","cx-stage-wrap");const header=make("div","cx-stage-header");
 put(header,make("div","",null));put(header.firstChild,make("h2","","Connection map"),make("p","","Curved lines link the selected research concept to related records; tap any node to explain or follow it."));
 const mode=make("div","cx-mode-tabs");for(const [m,label] of [["map","Map"],["path","Trace a path"]]){const b=clickable(label,()=>{conn.mode=m;render();},"cx-mode"+(conn.mode===m?" active":""));b.setAttribute("aria-pressed",String(conn.mode===m));put(mode,b);}put(header,mode);put(section,header);
 if(conn.mode==="path"){connPathView(section,focus);put(root,section);return;}
 const stage=make("div","cx-stage"),svg=document.createElementNS("http://www.w3.org/2000/svg","svg");svg.setAttribute("class","cx-curves");svg.setAttribute("aria-hidden","true");
 const main=connMainCard(focus,all),grid=make("div","cx-nodes");grid.id="cx-nodes";
 shown.forEach(c=>put(grid,connNeighborCard(c,focus.id)));
 put(stage,svg,main,grid);put(section,stage);
 const below=make("div","cx-stage-foot");put(below,make("p","cx-count","Showing "+shown.length+" of "+filtered.length+" matching connected concepts."));
 if(shown.length<filtered.length)put(below,clickable("Show more connections ("+(filtered.length-shown.length)+" remaining)",()=>{conn.limit=Math.min(filtered.length,conn.limit+10);render();},"cx-btn"));
 put(section,below);put(root,section);
 if(conn.observer){conn.observer.disconnect();conn.observer=null;}
 const draw=()=>{if(stage.isConnected)connDrawCurves(stage,svg,shown,focus.id);};
 requestAnimationFrame(draw);
 if(typeof ResizeObserver!=="undefined"){conn.observer=new ResizeObserver(draw);conn.observer.observe(stage);}
}
function connDrawCurves(stage,svg,shown,focusId){const rect=stage.getBoundingClientRect(),hub=stage.querySelector("#cx-hub");if(!hub||rect.width<10)return;
 const hb=hub.getBoundingClientRect();svg.replaceChildren();svg.setAttribute("viewBox","0 0 "+rect.width+" "+rect.height);svg.setAttribute("preserveAspectRatio","none");
 const defs=document.createElementNS("http://www.w3.org/2000/svg","defs");
 for(const [group,,color] of CONN_GROUPS){const mark=document.createElementNS("http://www.w3.org/2000/svg","marker");for(const [k,v] of Object.entries({id:"cx-tip-"+group,viewBox:"0 0 10 10",refX:"9",refY:"5",markerWidth:"5",markerHeight:"5",orient:"auto-start-reverse"}))mark.setAttribute(k,v);
 const shape=document.createElementNS("http://www.w3.org/2000/svg","path");shape.setAttribute("d","M 0 0 L 10 5 L 0 10 z");shape.setAttribute("fill",color);mark.append(shape);defs.append(mark);}svg.append(defs);
 for(const c of shown){const elem=stage.querySelector('[data-node-id="'+c.id+'"]');if(!elem)continue;const box=elem.getBoundingClientRect();
 let x1=hb.right-rect.left-2,y1=hb.top-rect.top+hb.height/2,x2=box.left-rect.left+2,y2=box.top-rect.top+box.height/2;
 if(x2<x1){x1=hb.left-rect.left;y1=hb.top-rect.top+hb.height/2;x2=box.right-rect.left;y2=box.top-rect.top+box.height/2;}
 const dep=c.primary.flow==="dependency";
 const arrowToHub=dep&&c.primary.to===focusId;
 if(arrowToHub)[x1,x2,y1,y2]=[x2,x1,y2,y1];
 const mx=(x1+x2)/2,curve="M"+x1+","+y1+" C"+mx+","+y1+" "+mx+","+y2+" "+x2+","+y2;
 const line=document.createElementNS("http://www.w3.org/2000/svg","path");
 line.setAttribute("d",curve);line.setAttribute("fill","none");line.setAttribute("stroke",connColor(c.group));line.setAttribute("stroke-width",conn.selected===c.id?"3.1":"1.7");line.setAttribute("opacity",conn.selected&&conn.selected!==c.id?".18":".67");line.setAttribute("class","cx-curve");
 if(!dep)line.setAttribute("stroke-dasharray","5 5");else line.setAttribute("marker-end","url(#cx-tip-"+c.group+")");
 svg.append(line);
 }
}
function connEdgeExplanation(c,focusId){const div=make("div","cx-edge-explanation");
 put(div,make("div","cx-explainer-header",null));put(div.firstChild,chip(connGroupName(c.group)),chip(statusName(c.n.status),statusClass(c.n.status)));
 put(div,make("h3","",c.n.title),make("p","cx-detail-summary",c.n.summary||"No description recorded."));
 for(const e of c.edges){const line=make("div","cx-edge-description");put(line,make("strong","",e.from+" — "+e.relation+" → "+e.to),make("p","",e.rationale||"No explanation recorded for this link."),make("small","",connRelationshipLabel(e,focusId)+" · "+(e.kind||"other")+" · editorial strength "+e.weight+"/5"));put(div,line);}
 const a=make("div","cx-inspect-actions");put(a,clickable("Open full research record",()=>openNode(c.id),"cx-btn"),clickable("Make this the center",()=>connGo(c.id),"cx-btn primary"));put(div,a);
 return div;}
function connExplain(root,focus,shown,filtered){const panel=make("section","cx-explanation");panel.id="cx-explanation";
 const selected=filtered.find(x=>x.id===conn.selected)||shown[0];if(selected){put(panel,make("p","eyebrow","WHY THESE CONCEPTS ARE CONNECTED"),connEdgeExplanation(selected,focus.id));}
 else put(panel,make("div","cx-no-results","No relationships match this filter. Choose another category."));
 put(root,panel);
 const foot=make("div","cx-method-note");put(foot,make("strong","","Reading rule: "),make("span","","Arrowheads show the recorded direction of dependency; dotted curves show associations. Neither arrows nor editorial weights establish causality, correlation, statistical confidence, or an equivalent forecasting horizon."));put(root,foot);}
function connPathBetween(start,target){if(!node(start)||!node(target))return null;if(start===target)return {ids:[start],edges:[]};
 const q=[{id:start,ids:[start],edges:[]}],seen=new Set([start]);let idx=0;
 while(idx<q.length){const cur=q[idx++];if(cur.edges.length>=6)continue;
 const next=[...(state.adj.get(cur.id)||[])].sort((a,b)=>b.weight-a.weight||a.kind.localeCompare(b.kind));
 for(const e of next){const other=e.from===cur.id?e.to:e.from;if(seen.has(other)||!node(other))continue;
 const route={id:other,ids:[...cur.ids,other],edges:[...cur.edges,e]};if(other===target)return route;
 seen.add(other);q.push(route);
 }}return null;}
function connPathView(root,focus){const panel=make("div","cx-trace-panel"),head=make("div","cx-trace-selects"),left=make("div","cx-trace-control"),right=make("div","cx-trace-control");
 put(left,make("label","", "From research concept"),connOptions(focus.id,connGo,"Trace path starting concept"));
 if(!node(conn.target)||conn.target===focus.id)conn.target=focus.id==="SRC-PRED"?"FIND-PEAK":"SRC-PRED";
 put(right,make("label","","To related concept"),connOptions(conn.target,x=>{conn.target=x;render();},"Trace path target concept"));
 put(head,left,right);put(panel,head);
 const route=connPathBetween(focus.id,conn.target);if(!route)put(panel,make("div","cx-no-results","No explanation path was found within six relationships. Try a closer pair of concepts."));
 else{put(panel,make("p","cx-path-count",route.edges.length+" documented relationship"+(route.edges.length===1?"":"s")+" in this route."));const steps=make("div","cx-path-steps");
 route.ids.forEach((id,i)=>{const rec=node(id),card=make("div","cx-path-step");put(card,make("span","cx-node-kind",readable(rec.type)),clickable(rec.title,()=>connGo(id),"cx-path-title"));put(steps,card);if(i<route.edges.length){const e=route.edges[i],forward=e.from===id&&e.to===route.ids[i+1],dep=e.flow==="dependency";
 const link=make("div","cx-path-connection");put(link,make("span","cx-path-arrow",dep?(forward?"↓":"↑"):"↕"),make("strong","",e.relation),make("p","",truncate(e.rationale,260)),make("small","",dep?(forward?"Following stored dependency direction":"Traversing backward against stored direction; not a causal inference"):"Association only; not causal or directional evidence"));put(steps,link);}});put(panel,steps);}
 put(root,panel,make("div","cx-method-note","Explanation paths follow existing graph links in either direction for discovery. Paths do not establish a statistical result, causality or operational forecast equivalence."));}
function renderConnectionExplorer(root){const focus=node(state.graphFocus)||node("FIND-OVERALL");if(!node(state.graphFocus))state.graphFocus=focus.id;
 connGraphHeading(root);const toolbar=make("div","cx-toolbar"),controls=make("div","cx-focus-control");
 const mainPicker=connOptions(focus.id,connGo,"Research focus concept");mainPicker.id="cx-focus-picker";put(controls,make("label","", "Research focus"),mainPicker);put(toolbar,controls);
 const actions=make("div","cx-toolbar-actions");
 const back=clickable("← Back",connStepBack,"cx-btn");back.disabled=conn.trail.length<2;
 put(actions,back,clickable("Reset",connReset,"cx-btn"),clickable("Copy link",()=>copyText(location.origin+location.pathname+"#graph="+encodeURIComponent(focus.id)),"cx-btn primary"));put(toolbar,actions);put(root,toolbar);
 if(conn.trail.length>1){const trail=make("div","cx-breadcrumbs");conn.trail.slice(-5).forEach((id,i)=>{if(i)put(trail,make("span","cx-crumb-sep","›"));put(trail,clickable(truncate(node(id)?.title||id,30),()=>connGo(id),"cx-crumb"));});put(root,trail);}
 const all=connLinks(focus.id);if(!CONN_FILTERS.includes(conn.filter))conn.filter="all";connFacetBar(root,all);
 const filtered=all.filter(c=>conn.filter==="all"||c.group===conn.filter);const shown=conn.filter==="all"?connBalanced(filtered,conn.limit):filtered.slice(0,conn.limit);
 connDiagram(root,focus,all,filtered,shown);if(conn.mode==="map")connExplain(root,focus,shown,filtered);
}
