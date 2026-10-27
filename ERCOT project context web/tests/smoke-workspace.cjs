/* Playwright functional coverage for Milestone 2.
   Run from repository root against local Python HTTP server on port 8765. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const {chromium}=require("playwright");
const BASE="http://127.0.0.1:8765/ERCOT%20project%20context%20web/explorer.html";
(async()=>{
 const browser=await chromium.launch({headless:true}),failures=[];
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});
 page.on("pageerror",e=>failures.push(e.message));
 page.on("console",m=>{if(m.type()==="error")failures.push(m.text());});
 try{
  await page.goto(BASE+"#workspace",{waitUntil:"networkidle"});
  await page.getByRole("heading",{name:"Assemble an evidence-backed explanation"}).waitFor();
  assert.equal(await page.locator("#ws-focus").inputValue(),"FIND-PEAK");
  assert.ok(await page.locator(".ws-evidence-card").count()>1);
  assert.match(await page.locator(".ws-main").innerText(),/Scientific qualifications/);
  await page.screenshot({path:"/tmp/ercot-workspace-desktop.png",fullPage:true});
  console.log("PASS: workspace loads selected finding, metrics, figures and caveats");

  await page.getByRole("button",{name:"Add connected evidence"}).click();
  const selected=await page.locator(".ws-packet-item").count();
  assert.ok(selected>=3,"expected at least 3 nodes in evidence bundle");
  assert.match(await page.locator(".ws-packet").innerText(),/Included evidence/);
  console.log("PASS: packet auto-collects authored direct evidence");

  await page.locator(".ws-input").nth(0).fill("Peak-hour research narrative");
  await page.locator(".ws-input").nth(1).fill("Data Visualizer");
  await page.locator("textarea.ws-input").fill("Explain why the ranking shifts at the retrospectively identified highest-demand hours.");
  const [download]=await Promise.all([page.waitForEvent("download"),page.getByRole("button",{name:"Export JSON"}).click()]);
  assert.match(download.suggestedFilename(),/ERCOT_research_packet_\d{4}-\d\d-\d\d\.json/);
  const jsonBytes=fs.readFileSync(await download.path());
  const exported=JSON.parse(jsonBytes.toString("utf8"));
  assert.equal(exported.schema,"ercot-research-packet/v1");
  assert.equal(exported.status,"draft-human-review");
  assert.equal(exported.title,"Peak-hour research narrative");
  assert.equal(exported.speaker,"Data Visualizer");
  assert.ok(exported.research_records.length>=3);
  assert.deepEqual(exported.research_records.map(n=>n.id),exported.selected_node_ids);
  assert.ok(exported.limitation_ids.length>=1,"required caveat not exported");
  assert.ok(exported.metric_ids.length>=1,"required numerical evidence not exported");
  assert.ok(exported.figure_ids.length>=1,"required source figure not exported");
  assert.ok(exported.source_references.every(ref=>ref.availability.includes("reference-only")));
  assert.match(exported.studio_s_importer_compatibility,/NOT a native Studio S/);
  console.log("PASS: JSON export preserves evidence and scientific review flags");
  const [md]=await Promise.all([page.waitForEvent("download"),page.getByRole("button",{name:"Export review notes"}).click()]);
  const markdown=fs.readFileSync(await md.path(),"utf8");
  assert.match(markdown,/Scientific review safeguards/);
  assert.match(markdown,/retrospective/i);
  console.log("PASS: human-readable review notes export");

  await page.getByRole("button",{name:"Trace to sources"}).click();
  await page.getByRole("heading",{name:/Trace to source records/}).waitFor();
  assert.ok(await page.locator(".ws-trail").count()>=1);
  console.log("PASS: source explanation paths visible");
  await page.getByRole("button",{name:"Change impact"}).click();
  await page.getByRole("heading",{name:/Downstream dependency review/}).waitFor();
  assert.match(await page.locator(".ws-main").innerText(),/review queue follows explicit outgoing dependency/);
  console.log("PASS: directed dependency review with scientific caveat");

  await page.reload({waitUntil:"networkidle"});
  await page.getByRole("heading",{name:"Assemble an evidence-backed explanation"}).waitFor();
  assert.equal(await page.locator(".ws-packet-item").count(),selected);
  assert.equal(await page.locator(".ws-input").first().inputValue(),"Peak-hour research narrative");
  console.log("PASS: locally persisted packet survives reload");

  page.once("dialog",d=>d.accept());
  await page.getByRole("button",{name:"Clear packet"}).click();
  assert.equal(await page.locator(".ws-packet-item").count(),0);
  await page.locator("#ws-import-file").setInputFiles({name:"sample.json",mimeType:"application/json",buffer:jsonBytes});
  assert.equal(await page.locator(".ws-packet-item").count(),selected);
  console.log("PASS: validate and restore portable packet");

  const unsafe={...exported,selected_node_ids:["NONEXISTENT_NODE"]};
  await page.locator("#ws-import-file").setInputFiles({name:"unknown.json",mimeType:"application/json",buffer:Buffer.from(JSON.stringify(unsafe))});
  assert.equal(await page.locator(".ws-packet-item").count(),selected,"invalid import must not replace current packet");
  console.log("PASS: reject unknown IDs on import");

  await page.getByRole("button",{name:"Evidence and caveats"}).click();
  const btn=page.locator(".ws-evidence-card .ws-card-actions button").filter({hasText:"Inspect"}).first();
  await btn.click();
  await page.getByRole("dialog",{name:/Research details/}).waitFor();
  await page.getByRole("button",{name:"Trace evidence"}).click();
  await page.getByRole("heading",{name:/Trace to source records/}).waitFor();
  console.log("PASS: jump from detail drawer into trace mode");

  const mobile=await browser.newPage({viewport:{width:390,height:844}});
  mobile.on("pageerror",e=>failures.push(e.message));
  await mobile.goto(BASE+"#workspace",{waitUntil:"networkidle"});
  await mobile.getByRole("heading",{name:"Assemble an evidence-backed explanation"}).waitFor();
  const size=await mobile.evaluate(()=>({body:document.documentElement.scrollWidth,view:innerWidth}));
  assert.ok(size.body<=size.view+2,"mobile horizontal overflow "+JSON.stringify(size));
  await mobile.screenshot({path:"/tmp/ercot-workspace-mobile.png",fullPage:true});
  assert.ok(await mobile.locator(".ws-packet").isVisible());
  assert.ok(await mobile.locator(".ws-evidence-card").count()>1);
  console.log("PASS: mobile evidence workspace and packet with no overflow");

  assert.deepEqual(failures,[]);
  console.log("PASS: no browser exceptions or console errors");
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
