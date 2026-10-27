/* ERCOT Research Explorer · Milestone 2 evidence workspace.
   This is a human-review drafting aid, NOT a scientific inference engine
   or a native Studio S importer. All facts retain their source node IDs. */
"use strict";
const WS_KEY="ercot-research-packet-v1";
const WS_SCHEMA="ercot-research-packet/v1";
const WS_LIMIT=60;
const ws={focus:"FIND-PEAK",mode:"evidence",packet:{schema:WS_SCHEMA,title:"ERCOT research evidence packet",speaker:"",notes:"",items:[]},saved:false};
function wsInfo(t){return make("div","ws-explain",t);}
function wsSave(){try{localStorage.setItem(WS_KEY,JSON.stringify(ws.packet));ws.saved=true;return true;}catch(_){ws.saved=false;return false;}}
function wsLoad(){try{let raw=localStorage.getItem(WS_KEY);if(!raw)return;let data=JSON.parse(raw);if(!data||data.schema!==WS_SCHEMA||!Array.isArray(data.items))return;ws.packet.title=String(data.title||ws.packet.title).slice(0,180);ws.packet.speaker=String(data.speaker||"").slice(0,120);ws.packet.notes=String(data.notes||"").slice(0,5000);ws.packet.items=[...new Set(data.items.filter(id=>typeof id==="string"&&node(id)))].slice(0,WS_LIMIT);ws.saved=true;}catch(_){/* private/local storage may be blocked */}}
function wsItems(){return ws.packet.items.map(node).filter(Boolean);}
function wsAdd(id,silent=false){if(!node(id))return false;if(ws.packet.items.includes(id)){if(!silent)toast("Already in the research packet");return false;}if(ws.packet.items.length>=WS_LIMIT){toast("Maximum "+WS_LIMIT+" research records per packet");return false;}ws.packet.items.push(id);wsSave();if(!silent)toast("Added "+id+" to research packet");if(state.view==="workspace"&&!state.selected)render();return true;}
function wsRemove(id){ws.packet.items=ws.packet.items.filter(x=>x!==id);wsSave();render();}
function wsAddFocus(id){ws.focus=id;linkView("workspace");}
function wsGrouped(id){const rows=uniqueNeighbors(id);
 const relevant=type=>rows.filter(e=>e.otherNode.type===type);
 const figures=relevant("visual");const metrics=relevant("metric");
 const limits=relevant("limitation");const sources=relevant("source");
 const questions=rows.filter(e=>["question","appendix_question"].includes(e.otherNode.type));
 const findings=relevant("finding");
 return {figures,metrics,limits,sources,questions,findings};
}
function wsBundle(id){const g=wsGrouped(id);const ids=[id,...g.metrics.slice(0,10).map(e=>e.other),...g.figures.slice(0,6).map(e=>e.other),...g.limits.slice(0,6).map(e=>e.other)];
 let count=0;ids.forEach(x=>{if(wsAdd(x,true))count++;});
 toast(count+" linked evidence records added");if(state.view==="workspace")render();}
function wsDirection(e,id){return e.to===id?"Points to selected research claim":"Selected record points toward linked concept";}
function wsCite(name,loc){const e=make("div","ws-source-ref");put(e,make("strong","",name||"Unspecified source"),make("span","",loc||"Location not recorded"));return e;}
function wsEdgeCard(e){const d=make("div","ws-evidence-card");const head=make("div","ws-evidence-top"),meta=make("div","card-meta");
 put(meta,chip(readable(e.otherNode.type)),chip(statusName(e.otherNode.status),statusClass(e.otherNode.status)));
 put(head,meta);const actions=make("div","ws-card-actions");
 put(actions,clickable("Inspect",()=>openNode(e.other),"action-button"),clickable(ws.packet.items.includes(e.other)?"Included ✓":"Add +",()=>{wsAdd(e.other);render();},"action-button"));
 put(d,head,make("h3","card-title",e.otherNode.title),make("p","card-copy",truncate(e.otherNode.summary,360)),make("div","ws-edge-explanation","Relationship: "+e.relation+" · "+wsDirection(e,ws.focus)),actions);
 if(e.otherNode.type==="visual"&&figSrc(e.otherNode)){const image=make("img","ws-thumb");image.loading="lazy";image.src=figSrc(e.otherNode);image.alt=e.otherNode.title;d.insertBefore(image,actions);}
 if(e.otherNode.type==="metric"&&typeof e.otherNode.value==="number"){const v=make("div","ws-metric-number",number(e.otherNode.value,3)+" "+(e.otherNode.unit||""));d.insertBefore(v,actions);}
 return d;}
function wsGroupSection(root,title,arr,hint){const sec=make("section","ws-group");const hd=make("div","section-head");put(hd,make("div","",null));hd.firstChild.append(make("h2","",title),make("p","",hint));put(sec,hd);
 if(arr.length){const grid=make("div","ws-evidence-grid");arr.forEach(e=>put(grid,wsEdgeCard(e)));put(sec,grid);}
 else put(sec,make("p","ws-no-edges","No direct "+title.toLowerCase()+" associated with this record. Do not assume the claim has this type of support."));
 put(root,sec);return sec;}
function wsPathFromClaim(startId,targetType,maxDepth=4){
 const queue=[{id:startId,path:[startId]}],seen=new Set([startId]),candidates=[];
 while(queue.length){
  const curr=queue.shift();if(curr.path.length>maxDepth+1)continue;
  if(curr.id!==startId && node(curr.id)?.type===targetType){candidates.push(curr.path);if(candidates.length>=8)break;continue;}
  for(const e of uniqueNeighbors(curr.id)){
   if(!["evidence","quantitative","provenance","dataflow","reasoning","original-link"].includes(e.kind))continue;
   if(seen.has(e.other))continue;
   seen.add(e.other);queue.push({id:e.other,path:[...curr.path,e.other]});
  }
 }
 return candidates;
}
function wsImpact(startId,depth=3){let visited=new Set([startId]),wave=[{id:startId,path:[startId]}],items=[];
 for(let i=0;i<depth;i++){
  const next=[];for(const cur of wave){for(const e of state.adj.get(cur.id)||[]){if(e.from!==cur.id||e.flow!=="dependency"||visited.has(e.to))continue;visited.add(e.to);const item={id:e.to,path:[...cur.path,e.to],relation:e.relation};items.push(item);next.push(item);}}
  wave=next;
 }return items.slice(0,90);
}
function wsTrail(root,id){const paths=wsPathFromClaim(id,"source",4),section=make("section","ws-group");heading(section,"Trace to source records");
 put(section,wsInfo("These are graph-based explanation routes through documented relationships, not causal paths, statistical proofs, or independent verification of source contents."));
 if(!paths.length)put(section,make("div","empty","No short documented route to a source node was found. Use the node's recorded source references."));
 paths.forEach((path,i)=>{const line=make("div","ws-trail");put(line,make("span","ws-trail-rank","PATH "+(i+1)));path.forEach((id,j)=>{if(j)put(line,make("span","ws-trail-arrow","→"));put(line,clickable(node(id)?.title||id,()=>openNode(id),"ws-trail-node"));});put(section,line);});put(root,section);}
function wsImpactsView(root,id){const list=wsImpact(id,3);const section=make("section","ws-group");heading(section,"Downstream dependency review · "+list.length+" records");
 put(section,wsInfo("This review queue follows explicit outgoing dependency edges for up to three steps. It indicates records to re-check after a change; it does not establish causality or guarantee that every dependent item is listed."));
 if(!list.length)put(section,make("div","empty","No downstream dependency records found within three steps."));
 const grid=make("div","ws-impact-list");list.forEach(item=>{const rec=node(item.id),button=make("button","related-item"),l=make("span");put(l,make("strong","",rec?.title||item.id),make("small","",readable(rec?.type)+" · "+item.relation+" · "+(item.path.length-1)+" steps"));put(button,l,make("span","","↗"));button.addEventListener("click",()=>wsSelect(item.id));put(grid,button);});put(section,grid);put(root,section);}
function wsSelect(id){if(!node(id))return;ws.focus=id;render();const focus=$("ws-focus");if(focus)focus.focus();}
function wsOptionSelect(){const select=make("select","ws-select");select.id="ws-focus";select.setAttribute("aria-label","Select research focus");
 const primary=["finding","visual","model","metric","limitation"];const headings=[["Key findings",nodesOfType("finding")],["Figures",nodesOfType("visual")],["Models",nodesOfType("model")],["Metrics",nodesOfType("metric")],["Limitations",nodesOfType("limitation")],["Other graph records",state.graph.nodes.filter(n=>!primary.includes(n.type))]];
 if(!node(ws.focus))ws.focus="FIND-PEAK";
 headings.forEach(([label,items])=>{const optgroup=make("optgroup");optgroup.label=label;items.forEach(n=>{const option=make("option","",n.title);option.value=n.id;if(n.id===ws.focus)option.selected=true;put(optgroup,option);});put(select,optgroup);});
 select.value=ws.focus;select.addEventListener("change",()=>wsSelect(select.value));return select;}
function wsControlTextarea(label,field,placeholder){const wrapper=make("label","ws-label"),input=make(field==="notes"?"textarea":"input","ws-input");input.value=ws.packet[field]||"";input.placeholder=placeholder;input.maxLength=field==="notes"?5000:field==="speaker"?120:180;if(field==="notes"){input.rows=4;}else input.type="text";input.addEventListener("input",()=>{ws.packet[field]=input.value;wsSave();});put(wrapper,make("span","",label),input);return wrapper;}
function wsPacketPanel(){const panel=make("aside","ws-packet");const header=make("div","ws-packet-head");
 put(header,make("div","",null));put(header.firstChild,make("p","eyebrow","PRESENTATION RESEARCH PACKET"),make("h2","",ws.packet.items.length+" selected records"));
 put(panel,header,wsControlTextarea("Packet title","title","What are you preparing to explain?"),wsControlTextarea("Speaker / reviewer (optional)","speaker","Leave blank until assigned"));
 const sec=make("div","ws-packet-items");put(sec,make("h3","","Included evidence"));
 const recs=wsItems();if(!recs.length)put(sec,make("p","ws-no-edges","No records selected. Start with a finding, then add its evidence, figures, and scientific limitations."));
 else recs.forEach(n=>{const row=make("div","ws-packet-item"),txt=make("div");put(txt,make("strong","",n.title),make("small","",n.id+" · "+readable(n.type)));const rm=clickable("×",()=>wsRemove(n.id),"ws-remove");rm.setAttribute("aria-label","Remove "+n.title);put(row,txt,rm);put(sec,row);});
 put(panel,sec,wsPacketAudit(),wsControlTextarea("Narration planning notes (optional)","notes","What should the audience understand? Which wording needs teammate approval?"));
 const sceneAction=clickable("Create presentation scene",sceneCreateFromPacket,"scene-primary");sceneAction.disabled=!ws.packet.items.length;sceneAction.title="Create an editable scene from the selected research packet";put(panel,sceneAction);
 const actions=make("div","ws-export-actions");const j=clickable("Export JSON",()=>wsExport("json"),"action-button"),md=clickable("Export review notes",()=>wsExport("md"),"action-button"),clear=clickable("Clear packet",wsClear,"action-button");
 j.disabled=!ws.packet.items.length;md.disabled=!ws.packet.items.length;
 put(actions,j,md,clear);put(panel,actions);
 const importBox=make("div","ws-import");const input=make("input");input.type="file";input.accept=".json,application/json";input.id="ws-import-file";input.setAttribute("aria-label","Import an exported research packet JSON");input.addEventListener("change",async()=>{const file=input.files?.[0];if(file)await wsImport(file);input.value="";});put(importBox,make("label","ws-label","Import a previous research packet"),input,make("p","ws-help","The packet is saved only in this browser until you export it. JSON exports are for human review, not automatic Studio S import."));put(panel,importBox);
 return panel;}
function wsPacketAudit(){const box=make("div","ws-audit"),items=wsItems();const types=new Set(items.map(n=>n.type));put(box,make("h3","","Review readiness checklist"));
 for(const [type,label] of [["finding","Claim or finding"],["metric","Numerical evidence"],["visual","Supporting figure"],["limitation","Scientific limitation"]]){const ready=types.has(type),row=make("div","ws-audit-row");put(row,make("span","ws-audit-mark"+(ready?" ready":""),ready?"✓":"!"),make("span","",label));put(box,row);}
 put(box,make("p","ws-help","Presence checks do not validate scientific correctness or indicate confidence. Teammate approval and the original documents still need review."));return box;}
function wsClear(){if(!ws.packet.items.length)return;if(!confirm("Clear the current research packet? Export it first if you need to keep a copy."))return;ws.packet.items=[];wsSave();render();toast("Packet cleared");}
function wsExportData(){
 const items=wsItems().map(n=>({id:n.id,type:n.type,title:n.title,summary:n.summary||"",evidence_status:n.status||"open",sources:(n.sources||[]).map(s=>({file:s.file||"",locator:s.locator||""})),...(typeof n.value==="number"?{measurement:{value:n.value,unit:n.unit||"",metric:n.metric||"",context:n.context||""}}:{}),...(figSrc(n)?{figure_asset_path:n.asset_path,figure_notebook_cell:n.notebook_cell??null}:{}),research_question:n.research_question||null}));
 const types=t=>items.filter(n=>n.type===t).map(n=>n.id);
 const sourceRefs=new Map();items.forEach(n=>n.sources.forEach(s=>sourceRefs.set(s.file+"::"+s.locator,s)));
 const ids=new Set(items.map(n=>n.id));const relationships=state.graph.edges.filter(e=>ids.has(e.from)&&ids.has(e.to)).map(e=>({from:e.from,to:e.to,relation:e.relation,kind:e.kind,flow:e.flow,editorial_weight:e.weight}));
 return {schema:WS_SCHEMA,status:"draft-human-review",linked_relationships:relationships,research_source:"data/context_graph.json",metrics_source:"data/model_metrics.json",exported_at:new Date().toISOString(),title:ws.packet.title.trim()||"Untitled research packet",speaker:ws.packet.speaker.trim()||null,editorial_notes:ws.packet.notes,selected_node_ids:[...ws.packet.items],claim_ids:types("finding"),metric_ids:types("metric"),figure_ids:types("visual"),limitation_ids:types("limitation"),source_references:[...sourceRefs.values()].map(s=>({...s,availability:"reference-only; verify original separately"})),research_records:items,scientific_review_rules:["Retrospective peak-demand membership is not knowable in advance.","Matched target-hour evaluation does not prove equal forecast issuance constraints.","Relationship weights are editorial and are not probabilities, correlations, or confidence scores.","A documented source locator is not independent verification of original source contents."],studio_s_importer_compatibility:"not evaluated; this is NOT a native Studio S scene manifest"};
}
function wsMarkdown(data){let result=["# "+data.title,"","Status: DRAFT — human review required","Research records: "+data.research_records.length,"Speaker/reviewer: "+(data.speaker||"Not assigned"),"","## Working narration notes",data.editorial_notes||"No narration notes entered.","","## Selected evidence"];
 for(const n of data.research_records){result.push("","### "+n.title+" ("+n.id+")","Type: "+n.type+" · Evidence status: "+n.evidence_status,"",n.summary||"No summary recorded.");
 if(n.measurement)result.push("","Numeric observation: "+n.measurement.value+" "+n.measurement.unit+" · "+n.measurement.metric);
 if(n.research_question)result.push("","Research question: "+n.research_question);
 if(n.figure_asset_path)result.push("","Local notebook image: "+n.figure_asset_path);
 if(n.sources.length){result.push("","Source references:");n.sources.forEach(s=>result.push("- "+s.file+" — "+s.locator+" (original file must be checked)"));}}
 result.push("","## Included authored relationships");if(data.linked_relationships.length){data.linked_relationships.forEach(e=>result.push("- "+e.from+" → "+e.to+" · "+e.relation+" (type: "+e.kind+")"));}else result.push("No relationships among selected nodes are recorded.");
 result.push("","## Scientific review safeguards");data.scientific_review_rules.forEach(t=>result.push("- "+t));result.push("","## Presentation production note","This export preserves source-linked research IDs for review. It is not an approved script, audio plan, or validated Studio S importer format.","");
 return result.join("\n");}
function wsDownload(name,content,mime){const blob=new Blob([content],{type:mime}),url=URL.createObjectURL(blob),a=make("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);}
function wsExport(format){if(!ws.packet.items.length){toast("Add evidence before exporting");return;}const data=wsExportData();const base="ERCOT_research_packet_"+new Date().toISOString().slice(0,10);if(format==="json")wsDownload(base+".json",JSON.stringify(data,null,2),"application/json");else wsDownload(base+".md",wsMarkdown(data),"text/markdown");toast("Export prepared: "+format.toUpperCase());}
async function wsImport(file){if(file.size>1024*1024){toast("Import exceeds the 1 MB safety limit");return;}try{const d=JSON.parse(await file.text());if(d.schema!==WS_SCHEMA||!Array.isArray(d.selected_node_ids)||d.selected_node_ids.length>WS_LIMIT)throw Error("Unsupported packet version or record count");if(d.selected_node_ids.some(id=>typeof id!=="string"||!node(id)))throw Error("Packet contains an unknown research node ID");ws.packet={schema:WS_SCHEMA,title:String(d.title||"Imported research packet").slice(0,180),speaker:String(d.speaker||"").slice(0,120),notes:String(d.editorial_notes||"").slice(0,5000),items:[...new Set(d.selected_node_ids)]};wsSave();render();toast("Imported "+ws.packet.items.length+" research records");}catch(e){toast("Import rejected: "+String(e.message||e));}}
function wsFocusPanel(){const panel=make("section","ws-focus-panel"),selectLabel=make("label","ws-label");put(selectLabel,make("span","","Research focus"),wsOptionSelect());put(panel,selectLabel);
 const rec=node(ws.focus);if(!rec)return panel;const intro=make("div","ws-focus-summary");put(intro,make("div","card-meta",null));put(intro.firstChild,chip(readable(rec.type)),chip(statusName(rec.status),statusClass(rec.status)));put(intro,make("h2","",rec.title),make("p","",rec.summary||"No explanation available."));
 if(rec.type==="visual"&&figSrc(rec)){const im=make("img","ws-lead-image");im.src=figSrc(rec);im.alt=rec.title;im.loading="lazy";put(intro,im);}
 if(typeof rec.value==="number")put(intro,make("div","ws-metric-number",number(rec.value,3)+" "+(rec.unit||"")));
 const btns=make("div","ws-card-actions");put(btns,clickable(ws.packet.items.includes(rec.id)?"Already in packet ✓":"Add selected record",()=>wsAdd(rec.id),"action-button"),clickable("Add connected evidence",()=>wsBundle(rec.id),"action-button"),clickable("Full record",()=>openNode(rec.id),"action-button"));put(intro,btns);put(panel,intro);
 const tabs=make("div","pill-tabs ws-mode-tabs");[["evidence","Evidence and caveats"],["trace","Trace to sources"],["impact","Change impact"]].forEach(([key,label])=>{const b=clickable(label,()=>{ws.mode=key;render();},"");b.classList.toggle("active",ws.mode===key);b.setAttribute("aria-pressed",String(ws.mode===key));put(tabs,b);});put(panel,tabs);return panel;}
function renderWorkspace(root){
 put(root,sectionTitle("PRESENTATION / RESEARCH PACKETS","Assemble an evidence-backed explanation","Choose a research claim, verify its supporting figures and limitations, and collect only the records you want to present. Export the packet for teammate review before writing narration."));
 const content=make("div","ws-layout"),left=make("div","ws-main"),focus=wsFocusPanel();put(left,focus);const f=wsGrouped(ws.focus);
 if(ws.mode==="evidence"){
  wsGroupSection(left,"Numerical evidence",f.metrics,"Reported metrics connected to the selected concept");
  wsGroupSection(left,"Notebook figures",f.figures,"Visual investigations associated through research graph links");
  wsGroupSection(left,"Scientific qualifications",f.limits,"Caveats to preserve when interpreting or presenting these results");
  if(f.sources.length)wsGroupSection(left,"Source records",f.sources,"Authored graph source records; verify original files");
  const rec=node(ws.focus);if(rec?.sources?.length){const sec=make("section","ws-group");heading(sec,"Original document locators");put(sec,wsInfo("These entries are references only. The original DOCX, notebook or prediction CSV may not be bundled in the public repository."));rec.sources.forEach(s=>put(sec,wsCite(s.file,s.locator)));put(left,sec);}
 }else if(ws.mode==="trace"){wsTrail(left,ws.focus);const s=make("section","ws-group");heading(s,"Recorded source locators");(node(ws.focus)?.sources||[]).forEach(ref=>put(s,wsCite(ref.file,ref.locator)));if(!node(ws.focus)?.sources?.length)put(s,wsInfo("No direct source locator on this record; inspect linked concepts and their provenance."));put(left,s);}
 else wsImpactsView(left,ws.focus);
 put(content,left,wsPacketPanel());put(root,content);
 put(root,note("This workspace helps assemble evidence for human review. No research numbers or graph relationships are changed, and exported packets are not native Studio S files.",true));
}
