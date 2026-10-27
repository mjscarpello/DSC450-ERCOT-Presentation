/* ERCOT Research Explorer · Milestone 3: reviewed scene authoring.
 * This standalone, local-only research drafting tool does NOT compile Studio S projects.
 * Never infer scientific truth or approval from graph-link counts or confidence-like weights. */
"use strict";
const SCENE_SCHEMA="ercot-scene-sequence/v1";
const SCENE_STORAGE="ercot-research-scenes-v1";
const SCENE_MAX=30;
const SCENE_NODE_MAX=25;
const SCENE_TEXT_MAX=7000;
const sceneStore={schema:SCENE_SCHEMA,scenes:[],activeId:null};
const SCENE_FIELDS={claimIds:"finding",metricIds:"metric",figureIds:"visual",limitationIds:"limitation"};
const SCENE_LABELS={claimIds:"Research claims",metricIds:"Numerical evidence",figureIds:"Notebook figures",limitationIds:"Scientific qualifications"};
const SCENE_RULES=[
 "Review of the original scientific sources is a human attestation, not independent verification by this application.",
 "The observed highest-demand 1% is a retrospective evaluation subset, not advance-known demand.",
 "Matching forecast target hours does not establish identical forecasting issuance conditions or weather-data availability.",
 "Research graph relationship weights are editorial linkage, not probabilities, scientific confidence, correlation, or causation.",
 "Approved scene content is for editorial review only; no Studio S importer compatibility has been established."
];
function sceneTrim(s,max=SCENE_TEXT_MAX){return String(s??"").slice(0,max);}
function sceneEmptyReview(){return {status:"draft",reviewer:"",sourceChecked:false,numbersChecked:false,limitationsChecked:false,reviewedAt:null,contentStamp:null};}
function sceneIds(s){return [...new Set(["claimIds","metricIds","figureIds","limitationIds"].flatMap(k=>s[k]||[]))];}
function sceneSnapshot(s){const ids=sceneIds(s),arr=ids.map(id=>node(id)).filter(Boolean);const edges=state.graph.edges.filter(e=>ids.includes(e.from)&&ids.includes(e.to));return {
   scene_id:s.id,title:s.title,objective:s.objective,narrator:s.narrator,narration:s.narration,on_screen_text:s.onScreenText,notes:s.notes,
   selected_ids:{claims:[...s.claimIds],metrics:[...s.metricIds],figures:[...s.figureIds],limitations:[...s.limitationIds]},
   records:arr.map(n=>({id:n.id,type:n.type,title:n.title,summary:n.summary||"",status:n.status||"open",sources:(n.sources||[]).map(x=>({file:x.file||"",locator:x.locator||""})),...(typeof n.value==="number"?{value:n.value,unit:n.unit||"",metric:n.metric||""}:{}),...(figSrc(n)?{asset_path:n.asset_path}:{}),research_question:n.research_question||null})),
   authored_relationships:edges.map(e=>({from:e.from,to:e.to,kind:e.kind,relation:e.relation,flow:e.flow,editorial_weight:e.weight}))
};}
function sceneCanonical(s){return JSON.stringify(sceneSnapshot(s));}
function sceneStamp(s){let h=2166136261;const t=sceneCanonical(s);for(let i=0;i<t.length;i++){h^=t.charCodeAt(i);h=Math.imul(h,16777619);}return ("00000000"+(h>>>0).toString(16)).slice(-8);}
function sceneValid(s){const issues=[];if(!s.title.trim())issues.push("Scene title required");
 if(!s.objective.trim())issues.push("Learning objective required");
 if(!s.narration.trim())issues.push("Narration is missing");
 if(!s.onScreenText.trim())issues.push("On-screen statement is missing");
 for(const [k,label] of Object.entries(SCENE_LABELS))if(!(s[k]||[]).length)issues.push(label+" missing");
 if(!s.review.reviewer.trim())issues.push("Reviewer name required");
 if(!s.review.sourceChecked)issues.push("Original supporting sources not acknowledged");
 if(!s.review.numbersChecked)issues.push("Numerical interpretation not acknowledged");
 if(!s.review.limitationsChecked)issues.push("Scientific caveats not acknowledged");
 return issues;}
function sceneStatus(s){if(s.review.status!=="approved")return "draft";return s.review.contentStamp===sceneStamp(s)?"approved":"stale";}
function sceneInvalidate(s){if(s.review.status==="approved"){s.review.status="draft";s.review.contentStamp=null;s.review.reviewedAt=null;s.review.sourceChecked=false;s.review.numbersChecked=false;s.review.limitationsChecked=false;}}
function scenePersistence(){try{localStorage.setItem(SCENE_STORAGE,JSON.stringify(sceneStore));return true;}catch(_){return false;}}
function sceneSanitizeImport(d,allowApproval=false){
 if(!d||d.schema!==SCENE_SCHEMA||!Array.isArray(d.scenes)||d.scenes.length>SCENE_MAX)throw Error("Unsupported scene file version or scene count");
 let seen=new Set();
 let scenes=d.scenes.map((x,i)=>{
  if(!x||typeof x!=="object")throw Error("Invalid scene record");
  const id=String(x.id||"");if(!/^SCENE-[0-9]{3}$/.test(id)||seen.has(id))throw Error("Duplicate or invalid scene ID");seen.add(id);
  const s={id,title:sceneTrim(x.title,160),objective:sceneTrim(x.objective,600),narrator:sceneTrim(x.narrator,140),narration:sceneTrim(x.narration),onScreenText:sceneTrim(x.onScreenText,1800),notes:sceneTrim(x.notes,2500),review:sceneEmptyReview()};
  for(const [field,expectedType] of Object.entries(SCENE_FIELDS)){
   const a=x[field];if(!Array.isArray(a)||a.length>SCENE_NODE_MAX)throw Error("Invalid "+field+" selection");
   if(a.some(id=>typeof id!=="string"||!node(id)||node(id).type!==expectedType))throw Error("Unknown or mismatched research ID in "+field);
   s[field]=[...new Set(a)];
  }
  if(allowApproval&&x.review?.status==="approved"){
   s.review={status:"approved",reviewer:sceneTrim(x.review.reviewer,120),sourceChecked:Boolean(x.review.sourceChecked),numbersChecked:Boolean(x.review.numbersChecked),limitationsChecked:Boolean(x.review.limitationsChecked),reviewedAt:sceneTrim(x.review.reviewedAt,80),contentStamp:sceneTrim(x.review.contentStamp,20)};
   if(sceneStatus(s)!=="approved"||sceneValid(s).length)s.review=sceneEmptyReview();
  }else if(x.review?.reviewer)s.review.reviewer=sceneTrim(x.review.reviewer,120);
  return s;
 });
 return {schema:SCENE_SCHEMA,scenes,activeId:scenes.some(s=>s.id===d.activeId)?d.activeId:(scenes[0]?.id||null)};
}
function sceneLoad(){try{const raw=localStorage.getItem(SCENE_STORAGE);if(!raw)return;const d=sceneSanitizeImport(JSON.parse(raw),true);sceneStore.scenes=d.scenes;sceneStore.activeId=d.activeId;}catch(_){/* storage may be restricted or stale */}}
function sceneCurrent(){return sceneStore.scenes.find(s=>s.id===sceneStore.activeId)||null;}
function sceneNextId(){for(let i=1;i<=999;i++){const id="SCENE-"+String(i).padStart(3,"0");if(!sceneStore.scenes.some(s=>s.id===id))return id;}throw Error("No scene IDs remain");}
function sceneCreateFromPacket(){if(sceneStore.scenes.length>=SCENE_MAX){toast("Maximum "+SCENE_MAX+" scenes reached");return;}
 const ids=new Set(ws.packet.items);if(!ids.size&&node(ws.focus))ids.add(ws.focus);
 const refs=Object.fromEntries(Object.entries(SCENE_FIELDS).map(([k,v])=>[k,[...ids].filter(id=>node(id)?.type===v).slice(0,SCENE_NODE_MAX)]));
 const finding=node(refs.claimIds[0]);const id=sceneNextId();
 const s={id,title:finding?finding.title:"Untitled presentation scene",objective:"",narrator:"",narration:"",onScreenText:"",notes:"",...refs,review:sceneEmptyReview()};
 sceneStore.scenes.push(s);sceneStore.activeId=id;scenePersistence();linkView("scenes");toast("Scene "+id+" created from research packet");}
function sceneCreateBlank(){if(sceneStore.scenes.length>=SCENE_MAX){toast("Maximum "+SCENE_MAX+" scenes reached");return;}
 const s={id:sceneNextId(),title:"Untitled presentation scene",objective:"",narrator:"",narration:"",onScreenText:"",notes:"",claimIds:[],metricIds:[],figureIds:[],limitationIds:[],review:sceneEmptyReview()};
 sceneStore.scenes.push(s);sceneStore.activeId=s.id;scenePersistence();render();}
function sceneSelect(id){sceneStore.activeId=id;scenePersistence();render();}
function sceneMove(id,shift){const arr=sceneStore.scenes,i=arr.findIndex(s=>s.id===id),j=i+shift;if(i<0||j<0||j>=arr.length)return;[arr[i],arr[j]]=[arr[j],arr[i]];scenePersistence();render();}
function sceneRemove(id){if(!confirm("Delete scene "+id+"? Export your sequence first if needed."))return;sceneStore.scenes=sceneStore.scenes.filter(s=>s.id!==id);if(sceneStore.activeId===id)sceneStore.activeId=sceneStore.scenes[0]?.id||null;scenePersistence();render();}
function sceneEdit(s,key,value){if(sceneStatus(s)==="approved")return;value=sceneTrim(value,key==="onScreenText"?1800:key==="objective"?600:key==="title"?160:key==="narrator"?140:key==="notes"?2500:SCENE_TEXT_MAX);s[key]=value;sceneInvalidate(s);scenePersistence();}
function sceneSetRefs(s,field,values){if(sceneStatus(s)==="approved")return;s[field]=[...new Set(values)].slice(0,SCENE_NODE_MAX);sceneInvalidate(s);scenePersistence();render();}
function sceneReviewSet(s,field,value){if(sceneStatus(s)==="approved")return;s.review[field]=field==="reviewer"?sceneTrim(value,120):Boolean(value);scenePersistence();}
function sceneApprove(s){if(sceneStatus(s)==="approved"){toast("Already approved, return to draft before editing");return;}
 const issues=sceneValid(s);if(issues.length){sceneShowIssues(issues);return;}
 s.review.status="approved";s.review.reviewedAt=new Date().toISOString();s.review.contentStamp=sceneStamp(s);scenePersistence();render();toast("Editorial review recorded for "+s.id);}
function sceneReopen(s){sceneInvalidate(s);scenePersistence();render();toast("Approval revoked; scene returned to draft");}
function sceneShowIssues(arr){const b=$("scene-issues");if(b){b.replaceChildren();const ul=make("ul");arr.forEach(v=>put(ul,make("li","",v)));put(b,make("strong","","Review requirements"),ul);b.hidden=false;b.scrollIntoView({block:"nearest"});}else toast("Review incomplete: "+arr[0]);}
function sceneField(s,key,label,placeholder,textarea=false){const wrap=make("label","scene-field"),input=make(textarea?"textarea":"input","ws-input");input.value=s[key];input.maxLength=key==="title"?160:key==="objective"?600:key==="narrator"?140:key==="onScreenText"?1800:key==="notes"?2500:SCENE_TEXT_MAX;input.placeholder=placeholder;input.disabled=sceneStatus(s)==="approved";if(textarea){input.rows=key==="narration"?5:3;}else input.type="text";
 input.addEventListener("input",()=>sceneEdit(s,key,input.value));put(wrap,make("span","",label),input);return wrap;}
function sceneSection(title,desc){const s=make("section","scene-section");put(s,make("h3","",title));if(desc)put(s,make("p","scene-hint",desc));return s;}
function sceneRefs(s,field){const type=SCENE_FIELDS[field],section=sceneSection(SCENE_LABELS[field],"Choose the exact authoritative research records used in this scene.");const selected=make("div","scene-selected");
 s[field].forEach(id=>{const rec=node(id),pill=make("div","scene-reference"),b=clickable("×",()=>sceneSetRefs(s,field,s[field].filter(x=>x!==id)),"scene-ref-remove");b.disabled=sceneStatus(s)==="approved";b.setAttribute("aria-label","Remove "+rec.title+" from "+SCENE_LABELS[field]);
 const inspect=clickable(truncate(rec.title,95),()=>openNode(id),"scene-ref-title");put(pill,inspect,b);put(selected,pill);});
 if(!s[field].length)put(selected,make("p","scene-hint","No "+SCENE_LABELS[field].toLowerCase()+" selected."));
 put(section,selected);
 const row=make("div","scene-ref-picker"),choose=make("select","ws-select");choose.setAttribute("aria-label","Add "+SCENE_LABELS[field]);const intro=make("option","","Select a research record…");intro.value="";put(choose,intro);
 nodesOfType(type).sort((a,b)=>a.title.localeCompare(b.title)).forEach(n=>{if(s[field].includes(n.id))return;const op=make("option","",n.title);op.value=n.id;put(choose,op);});
 const add=clickable("Add record",()=>{if(choose.value)sceneSetRefs(s,field,[...s[field],choose.value]);},"action-button");add.disabled=sceneStatus(s)==="approved";
 put(row,choose,add);put(section,row);return section;}
function sceneReviewPanel(s){const sec=sceneSection("Scientific and editorial review","Only a named human reviewer can record completion. The application does not verify the truth of the source documents.");
 const status=sceneStatus(s),marker=make("div","scene-review-banner "+status);
 put(marker,make("strong","",status==="approved"?"Editorially approved":status==="stale"?"Previously approved evidence has changed":"Draft · not approved"),make("span","",status==="approved"?"Reviewed by "+s.review.reviewer+" on "+s.review.reviewedAt:"Approval is not automatic; resolve the checklist and confirm original sources."));put(sec,marker);
 if(status==="approved"){put(sec,clickable("Reopen scene for edits",()=>sceneReopen(s),"action-button"));return sec;}
 const rv=sceneField({reviewer:s.review.reviewer},"reviewer","Reviewer name","Name of person checking the original evidence");rv.querySelector("input").addEventListener("input",e=>sceneReviewSet(s,"reviewer",e.target.value));put(sec,rv);
 const checks=[["sourceChecked","I checked the original source files and their relevant locations."],["numbersChecked","I checked the reported numbers, comparison sample and forecast conditions."],["limitationsChecked","I reviewed limitations, including retrospective peak categories and possible forecast-origin differences."]];
 checks.forEach(([key,label])=>{const line=make("label","scene-check"),input=make("input");input.type="checkbox";input.checked=Boolean(s.review[key]);input.addEventListener("change",()=>sceneReviewSet(s,key,input.checked));put(line,input,make("span","",label));put(sec,line);});
 const errors=make("div","scene-errors");errors.id="scene-issues";errors.hidden=true;put(sec,errors);
 put(sec,clickable("Record editorial approval",()=>sceneApprove(s),"scene-primary"));
 put(sec,make("p","scene-hint","Approved scenes are read-only. Reopening or changing underlying research records invalidates approval. Imported scene files must be reviewed again."));return sec;}
function scenePreview(s){const sec=make("aside","scene-preview");put(sec,make("p","eyebrow","ON-SCREEN PREVIEW · CONCEPTUAL ONLY"));const slide=make("div","scene-slide"),pic=node(s.figureIds[0]);put(slide,make("div","scene-slide-head",s.title||"Scene title"));
 if(pic&&figSrc(pic)){const img=make("img","scene-slide-figure");img.src=figSrc(pic);img.alt=pic.title;put(slide,img);}else put(slide,make("div","scene-slide-empty","Add a notebook figure to preview it here."));
 put(slide,make("p","scene-slide-text",s.onScreenText||"On-screen statement appears here."));put(sec,slide);
 const points=make("div","scene-preview-meta");put(points,make("strong","","Research linked to this scene"),make("p","","Claims: "+s.claimIds.length+" · Metrics: "+s.metricIds.length+" · Figures: "+s.figureIds.length+" · Caveats: "+s.limitationIds.length));put(sec,points);
 const limits=make("div","scene-preview-limits");put(limits,make("strong","","Scientific qualifiers"));s.limitationIds.forEach(id=>put(limits,make("p","",node(id)?.title||id)));if(!s.limitationIds.length)put(limits,make("p","", "No limitation selected. This scene cannot be approved."));put(sec,limits);
 return sec;}
function sceneReviewEditor(s){const main=make("div","scene-editor-main"),head=make("div","scene-editor-head");put(head,make("p","eyebrow","SCENE "+s.id),chip(sceneStatus(s)==="approved"?"Editorially approved":"Draft",sceneStatus(s)==="approved"?"verified":"caution"));put(main,head);
 put(main,sceneField(s,"title","Scene title","What is this scene about?"),sceneField(s,"objective","Learning objective","What should the audience understand?"),sceneField(s,"narrator","Speaker (optional)","Who will deliver these lines?"),sceneField(s,"narration","Narration draft","Explain the result, why it matters and what the evidence actually supports.",true),sceneField(s,"onScreenText","On-screen statement","Concise takeaway shown to the audience",true));
 const sec=sceneSection("Linked research records","Attach only content relevant to this scene. Source-linked details are embedded in the export.");for(const field of Object.keys(SCENE_FIELDS))put(sec,sceneRefs(s,field));put(main,sec,sceneField(s,"notes","Presenter / editing notes","Visual emphasis, caption ideas, areas requiring team discussion",true),sceneReviewPanel(s));
 return main;}
function sceneList(){const panel=make("aside","scene-list-panel"),top=make("div","scene-list-header");put(top,make("h2","","Presentation sequence"),make("p","",sceneStore.scenes.length+" of "+SCENE_MAX+" scenes"));put(panel,top);
 const buttons=make("div","scene-list-actions");put(buttons,clickable("Add blank scene",sceneCreateBlank,"action-button"),clickable("From evidence packet",sceneCreateFromPacket,"action-button"));put(panel,buttons);
 const list=make("div","scene-list");sceneStore.scenes.forEach((s,i)=>{const row=make("div","scene-list-item"+(sceneStore.activeId===s.id?" active":"")),select=clickable((i+1)+". "+truncate(s.title,54),()=>sceneSelect(s.id),"scene-list-select"),tools=make("div","scene-order-tools");
 put(select,make("small","",s.id+" · "+(sceneStatus(s)==="approved"?"Approved":"Draft")));
 const up=clickable("↑",()=>sceneMove(s.id,-1),"scene-small-btn"),down=clickable("↓",()=>sceneMove(s.id,1),"scene-small-btn"),remove=clickable("×",()=>sceneRemove(s.id),"scene-small-btn");
 up.disabled=i===0;down.disabled=i===sceneStore.scenes.length-1;up.setAttribute("aria-label","Move "+s.id+" earlier");down.setAttribute("aria-label","Move "+s.id+" later");remove.setAttribute("aria-label","Delete "+s.id);
 put(tools,up,down,remove);put(row,select,tools);put(list,row);});put(panel,list);
 const totals=make("div","scene-list-footer");const approved=sceneStore.scenes.filter(s=>sceneStatus(s)==="approved").length;put(totals,make("p","","Editorially approved: "+approved+" / "+sceneStore.scenes.length));
 const exports=make("div","scene-export-actions");put(exports,clickable("Export JSON",()=>sceneExport("json"),"action-button"),clickable("Review notes",()=>sceneExport("md"),"action-button"));put(totals,exports);
 const input=make("input");input.type="file";input.accept=".json,application/json";input.setAttribute("aria-label","Import scene sequence JSON");input.addEventListener("change",async()=>{if(input.files?.[0])await sceneImport(input.files[0]);input.value="";});put(totals,make("label","ws-label","Import a scene sequence"),input,make("p","scene-hint","Drafts stay in this browser until exported. Importing always requires a fresh human review; no native Studio S project is created."));
 put(panel,totals);return panel;}
function sceneExportData(){const scenes=sceneStore.scenes.map((s,i)=>({...sceneSnapshot(s),order:i+1,review:{status:sceneStatus(s),reviewer:s.review.reviewer||null,sourceChecked:!!s.review.sourceChecked,numbersChecked:!!s.review.numbersChecked,limitationsChecked:!!s.review.limitationsChecked,reviewedAt:sceneStatus(s)==="approved"?s.review.reviewedAt:null,contentStamp:sceneStatus(s)==="approved"?s.review.contentStamp:null}}));
 return {schema:SCENE_SCHEMA,status:scenes.length&&scenes.every(s=>s.review.status==="approved")?"editorially-reviewed":"draft-human-review",exported_at:new Date().toISOString(),origin:"DSC 450 ERCOT Research Explorer",research_sources:{graph:"data/context_graph.json",metrics:"data/model_metrics.json"},studio_s_compatibility:"unverified — NOT a native Studio S v2 project or importer payload",scientific_review_rules:SCENE_RULES,scenes};}
function sceneMarkdown(data){const rows=["# ERCOT scene authoring review","", "**Status:** "+data.status,"**Source:** DSC 450 research graph","**Studio S:** not a native importer format",""];
 data.scenes.forEach(s=>{rows.push("## "+s.order+". "+s.title+" ("+s.scene_id+")","", "**Objective:** "+s.objective,"**Speaker:** "+(s.narrator||"Not assigned"),"**Review:** "+s.review.status+(s.review.reviewer?" ("+s.review.reviewer+")":""),"","### Narration",s.narration||"*Not written*","", "### On-screen statement",s.on_screen_text||"*Not written*","", "### Evidence");
 for(const rec of s.records){rows.push("- "+rec.id+" ["+rec.type+"; "+rec.status+"]: "+rec.title);for(const src of rec.sources)rows.push("  - Source: "+src.file+" ("+src.locator+")");}rows.push("","### Scientific qualifications");
 for(const id of s.selected_ids.limitations)rows.push("- "+(s.records.find(r=>r.id===id)?.title||id));
 rows.push("","### Presenter notes",s.notes||"None","");});
 rows.push("## Required scientific safeguards");SCENE_RULES.forEach(s=>rows.push("- "+s));rows.push("");return rows.join("\n");}
function sceneExport(type){if(!sceneStore.scenes.length){toast("Add a scene before exporting");return;}const d=sceneExportData();const base="ERCOT_scene_sequence_"+new Date().toISOString().slice(0,10);if(type==="json")wsDownload(base+".json",JSON.stringify(d,null,2),"application/json");else wsDownload(base+".md",sceneMarkdown(d),"text/markdown");toast("Scene sequence export prepared");}
async function sceneImport(file){if(file.size>2*1024*1024){toast("Scene JSON exceeds the 2 MB import limit");return;}try{const d=JSON.parse(await file.text());if(!Array.isArray(d.scenes))throw Error("Missing scene records");const src=d.scenes.map(x=>({id:x.scene_id||x.id,title:x.title,objective:x.objective,narrator:x.narrator,narration:x.narration,onScreenText:x.on_screen_text,notes:x.notes,
 claimIds:x.selected_ids?.claims||x.claimIds,metricIds:x.selected_ids?.metrics||x.metricIds,figureIds:x.selected_ids?.figures||x.figureIds,limitationIds:x.selected_ids?.limitations||x.limitationIds,review:{reviewer:x.review?.reviewer||""}}));const parsed=sceneSanitizeImport({schema:d.schema,scenes:src,activeId:src[0]?.id},false);
 if(!confirm("Replace all local scene drafts with the imported scenes? Imported approvals are reset for fresh review."))return;
 sceneStore.scenes=parsed.scenes;sceneStore.activeId=parsed.activeId;scenePersistence();render();toast("Imported "+parsed.scenes.length+" scenes as drafts");}catch(e){toast("Import rejected: "+String(e.message||e));}}
function renderScenes(root){put(root,sectionTitle("PRESENTATION / SCENE AUTHORING","Design an evidence-backed presentation","Compose ordered scenes with narration, on-screen explanations, authoritative figures, numerical evidence and limitations. Record human editorial review without changing the underlying research."));
 const layout=make("div","scene-layout");put(layout,sceneList());
 if(!sceneStore.scenes.length){const empty=make("div","scene-empty"),title=make("h2","","Start from your evidence packet");put(empty,title,make("p","","Open the Evidence Workspace, collect a finding and its metrics, figures and limitations, then create a linked scene. Or begin with a blank scene."),clickable("Create scene from packet",sceneCreateFromPacket,"scene-primary"),clickable("Start a blank scene",sceneCreateBlank,"action-button"));put(layout,empty);}
 else {const s=sceneCurrent()||sceneStore.scenes[0];sceneStore.activeId=s.id;put(layout,sceneReviewEditor(s),scenePreview(s));}
 put(root,layout,note("Scene approvals are explicit human editorial attestations. They do not verify upstream experiments or certify scientific truth. Exports are research-authoring documents, not executable Studio S projects.",true));}
