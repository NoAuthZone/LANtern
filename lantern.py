#!/usr/bin/env python3
"""LANtern — standalone DNS and DHCPv4 server with a dark browser console.

Requires Python 3.10+ on Windows 10/11, macOS, or Linux. No pip dependencies.
Run: python3 lantern.py
On macOS/Linux, service ports/interface binding normally require sudo.
Open the Console URL printed in the terminal; quit with Ctrl+C.
Settings and leases are saved in an automatically created data directory.
Use --help for port, data-directory, and browser options.
"""
from __future__ import annotations


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LANtern · Network services</title>
<style>
:root{color-scheme:dark;--bg:#0d1522;--card:#131f30;--line:#2a374b;--text:#e6edf8;--muted:#95a6be;--accent:#689bff;--warn:#dfba7c;--red:#f39ca6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}button,input,select,textarea{font:inherit}.sidebar{width:224px;position:fixed;inset:0 auto 0 0;background:#131f30;border-right:1px solid var(--line);padding:32px 18px;display:flex;flex-direction:column;z-index:5}.brand{display:flex;gap:10px;align-items:center;font-size:18px;font-weight:750;letter-spacing:-.5px;padding:0 5px 42px}.brand small{display:block;font-size:9px;color:#8c9db6;letter-spacing:1.6px;font-weight:600;margin-top:2px}.brand-symbol{background:var(--accent);color:#131f30;border-radius:11px;width:37px;height:39px;display:grid;place-items:center;font-size:26px;font-weight:750}.nav-label{color:#8396b1;font-size:10px;font-weight:700;letter-spacing:1.7px;padding:0 15px;margin-bottom:12px}.tabs{display:flex;flex-direction:column;gap:7px}.tabs button{border:0;background:transparent;display:flex;gap:8px;align-items:center;text-align:left;padding:12px 15px;color:#95a6be;font-weight:600;border-radius:8px}.tabs button:hover{background:#1c2b42}.tabs button.active{background:#213451;color:var(--accent)}.tabs button:before{content:"";width:6px;height:6px;border:1.5px solid #7289a8;border-radius:2px;margin-right:4px}.tabs button.active:before{background:var(--accent);border-color:var(--accent)}.nav-count{margin-left:auto;font-size:11px;background:#2a3c59;min-width:20px;padding:1px 6px;text-align:center;border-radius:5px}.sidebar-footer{margin-top:auto;border-top:1px solid var(--line);padding:22px 9px 0;font-size:12px;color:#a7b9d0}.sidebar-footer small{display:block;color:#8396b1;font-size:10px;padding-left:15px;margin-top:5px}.connection-dot{display:inline-block;width:6px;height:6px;background:#31ae86;border-radius:50%;margin-right:6px}header{margin-left:224px;border-bottom:1px solid var(--line);background:#131f30}header>div{max-width:1280px;margin:auto;padding:27px 36px;display:flex;justify-content:space-between;align-items:center;gap:20px}main{margin-left:224px;padding:28px 36px;max-width:1352px}h1{font-size:27px;line-height:1.25;font-weight:720;letter-spacing:-.8px;margin:5px 0 7px}h2{font-size:16px;letter-spacing:-.25px;font-weight:650;margin:0 0 8px}h3{font-size:15px;margin:22px 0 9px}.eyebrow{font-size:9px;letter-spacing:1.9px;color:#91a6c3;font-weight:700}.sub{margin:0;font-size:12px;color:var(--muted)}small,.hint{color:var(--muted)}.hint{font-size:12px;margin:7px 0;line-height:1.65}.buttons{display:flex;align-items:center;gap:9px;flex-wrap:wrap}button,.file-button{border:1px solid #33445d;border-radius:7px;background:#131f30;color:#b8c8dd;padding:9px 13px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s,border-color .15s,box-shadow .15s}button:hover,.file-button:hover{background:#1d2e47;border-color:#5b7ca8}button.primary{background:var(--accent);border-color:var(--accent);color:#131f30;box-shadow:0 2px 4px #2563eb1a}button.primary:hover{background:#4674e9}button.stop{color:var(--red);background:#38252d;border-color:#6b3b49}button:disabled{opacity:.45;cursor:not-allowed}button.compact{padding:7px 11px;font-size:11px}.status-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:22px}.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:24px;margin-bottom:22px;box-shadow:0 2px 3px #1b335103}.status-grid .card{margin:0;display:flex;justify-content:space-between;align-items:center;gap:10px;padding:22px 24px}.status-title{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:650}.service-icon{width:31px;height:31px;display:inline-grid;place-items:center;border-radius:8px;color:#8bb2ff;background:#213451;font-size:22px;font-weight:500}.service-icon.purple{color:#c19af6;background:#302545}.status-grid small{display:block;font-size:11px;margin:5px 0 0 40px}.badge{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:600;padding:3px 8px;border-radius:5px;background:#243349;color:#a6b5cb}.badge:before{content:"";width:4px;height:4px;border-radius:50%;background:currentColor}.badge.on{color:#77d8b1;background:#193c35}.badge.dirty{color:#f0c886;background:#3a2e20}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.grid.two{grid-template-columns:1fr 1fr}.field{display:flex;flex-direction:column;gap:7px}label{font-size:11px;font-weight:600;color:#b6c5db}input,select,textarea{width:100%;min-width:0;background:#101a2a;color:#e1eaf7;border:1px solid #35445e;border-radius:6px;padding:10px 11px;font-size:12px;line-height:1.4}input::placeholder,textarea::placeholder{color:#7286a3}input:focus,select:focus,textarea:focus{outline:2px solid #2d5087;outline-offset:1px;border-color:var(--accent)}input[readonly]{color:#9eafc6;background:#1a273a}textarea{resize:vertical;min-height:78px}.wide{grid-column:1/-1}.section-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:22px}.section-head h2{margin-bottom:3px}.section-head .hint{margin:3px 0 0}[hidden]{display:none!important}.panel{margin-bottom:20px}.panel>.card:first-child>h2{margin-bottom:20px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:12px}th{text-align:left;font-size:10px;font-weight:650;color:#9cadc7;background:#19273b;padding:10px 8px;border-bottom:1px solid var(--line);text-transform:uppercase;letter-spacing:.6px}td{padding:11px 8px;border-bottom:1px solid #29374d}td input,td select{padding:8px;min-width:85px;background:#131f30}td:first-child input{min-width:170px}#records td:nth-child(4){width:105px}#records td:last-child{width:80px}.remove{padding:6px 8px;color:#e2a0ae;border-color:#593747;font-size:10px;background:#131f30}.notice{padding:12px 14px;border:1px solid #5a4932;background:#30291f;border-radius:7px;font-size:12px;color:#e6c18b;margin:16px 0}.message{padding:12px 16px;border-radius:8px;margin-bottom:20px;background:#1a352e;border:1px solid #2e5b4a;color:#8ed4b5;font-size:12px;white-space:pre-wrap}.message.error{background:#3a242d;border-color:#794451;color:#f1adbb}.log-controls{display:grid;grid-template-columns:145px 1fr auto auto;gap:10px;margin-bottom:14px}.log{font:11px/1.85 ui-monospace,SFMono-Regular,Consolas,monospace;background:#090f1b;border:1px solid #2c3c56;border-radius:8px;height:380px;overflow:auto;padding:20px;white-space:pre-wrap;overflow-wrap:anywhere}.log-line{color:#b8c9e2}.log-line.warn{color:#f4ca89}.log-line.error{color:#ffb2b5}.empty{color:#91a6c3;padding:42px 20px;text-align:center;font-size:12px;background:#101a2a;border-radius:0 0 7px 7px}.foot{color:#8396b2;font-size:10px;line-height:1.8;margin:20px 0}a{color:var(--accent)}.inline-warning{color:#e7c185;background:#342d22;border-radius:6px;padding:9px 12px;font-size:12px;margin-top:10px}
@media(min-width:1577px){main{margin-right:auto}}
@media(max-width:1100px){.sidebar{width:192px;padding:28px 13px}.brand{font-size:16px;gap:8px}.brand-symbol{width:32px;height:35px}header,main{margin-left:192px}main,header>div{padding:24px}.status-grid .card{padding:18px}.status-title{font-size:13px;gap:6px}.status-grid small{margin-left:0}.service-icon{display:none}header>div{flex-wrap:wrap}}
@media(max-width:800px){.sidebar{position:static;width:auto;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:18px}.brand{padding:0 0 18px}.brand-symbol{width:32px;height:34px}.brand small{display:none}.nav-label,.sidebar-footer{display:none}.tabs{flex-direction:row;overflow:auto;gap:4px}.tabs button{padding:9px 11px;font-size:11px}.tabs button:before{display:none}.tabs button:first-child{margin-left:0}.nav-count{margin-left:2px}header,main{margin-left:0}header>div{padding:22px 18px;gap:17px}main{padding:20px 18px}h1{font-size:24px}.grid,.grid.two,.status-grid{grid-template-columns:1fr}.status-grid{gap:12px}.status-grid .card{padding:18px}.service-icon{display:inline-grid}.status-grid small{margin-left:40px}.card{padding:20px}.log-controls{grid-template-columns:1fr 1fr}.section-head{flex-wrap:wrap;gap:10px;margin-bottom:18px}.status-title{font-size:15px}}

.brand-symbol{color:#fff;background:#3769e9}button.primary{background:#3769e9;border-color:#4d7af2;color:#fff}button.primary:hover{background:#4675ee}
</style>
</head>
<body>
<aside class="sidebar">
<div class="brand"><span class="brand-symbol">L</span><div>LANtern<small>NETWORK SERVICES</small></div></div>
<div class="nav-label">WORKSPACE</div><nav class="tabs" aria-label="Workspace navigation"><button class="active" data-tab="dns" aria-selected="true">DNS</button><button data-tab="dhcp" aria-selected="false">DHCP</button><button data-tab="leases" aria-selected="false">Active leases <span id="leaseCount" class="nav-count">0</span></button><button data-tab="logs" aria-selected="false">Activity log</button></nav>
<div class="sidebar-footer"><span class="connection-dot"></span> Local workspace<small>Windows · macOS · Linux</small></div>
</aside>
<header><div><div><div class="eyebrow">NETWORK WORKSPACE</div><h1>Network services</h1><p class="sub">Manage address assignment, name resolution, and network activity.</p></div><div class="buttons"><span id="dirty" class="badge dirty" hidden>Unsaved changes</span><button id="stopAll">Stop all services</button><button id="save" class="primary">Save configuration</button></div></div></header>
<main>
<div id="message" class="message" role="status" hidden></div>
<div class="status-grid">
  <div class="card"><div><div class="status-title"><span class="service-icon">↗</span> DNS resolver <span id="dnsBadge" class="badge">Stopped</span></div><small id="dnsInfo">UDP + TCP · Port 53</small></div><button id="dnsToggle">Start DNS</button></div>
  <div class="card"><div><div class="status-title"><span class="service-icon purple">⇄</span> DHCP server <span id="dhcpBadge" class="badge">Stopped</span></div><small id="dhcpInfo">IPv4 · UDP 67 / 68</small></div><button id="dhcpToggle">Start DHCP</button></div>
</div>
<section class="card">
 <div class="section-head"><div><h2>Network interface</h2><div class="hint">Choose the adapter and static IPv4 address your services will use.</div></div><button id="refreshInterfaces" class="compact">Refresh interfaces</button></div>
 <div class="grid"><div class="field"><label for="iface">Adapter / IPv4 address</label><select id="iface"><option value="">Select an interface…</option></select></div><div class="field"><label for="bind_ip">Server IP address</label><input id="bind_ip" readonly></div><div class="field"><label for="netmask">Subnet mask</label><input id="netmask" readonly></div></div>
 <p class="hint">Use DHCP on a network you manage. Disable any existing DHCP server on that network before starting this one.</p>
 <div id="platformNote" class="notice" hidden>DHCP requires Windows 10/11, macOS, or Linux.</div>
 <div id="dnsWarning" class="inline-warning" hidden>DHCP advertises this DNS server, but the DNS service is stopped.</div>
</section>

<section class="panel" id="tab-dns">
 <div class="card"><h2>DNS settings</h2><div class="grid">
  <div class="field"><label for="dns_port">Listen port</label><input id="dns_port" type="number" min="1" max="65535"></div>
  <div class="field"><label for="dns_timeout">Forwarder timeout (seconds)</label><input id="dns_timeout" type="number" min="0.2" max="5" step="0.1"></div>
  <div class="field"><label for="local_zone">Local zone (optional)</label><input id="local_zone" placeholder="home.arpa"></div>
  <div class="field wide"><label for="forwarders">Upstream DNS servers</label><textarea id="forwarders" placeholder="1.1.1.1&#10;9.9.9.9"></textarea><small>One IP per line. Optional port: 192.168.1.1:5353 or [2606:4700:4700::1111]:53. Leave empty for local-only DNS. Up to four servers.</small></div>
 </div><p class="hint">Local records take priority. Unknown names in the local zone stay local. Upstream queries use your system routing.</p></div>
 <div class="card"><div class="section-head"><div><h2>Local DNS records</h2><div class="hint">Map names to your devices. Supports A, AAAA, CNAME, TXT, MX, PTR, and simple wildcards.</div></div><button id="addRecord">+ Add record</button></div><div class="table-wrap"><table><thead><tr><th>Name</th><th>Type</th><th>Value</th><th>TTL (s)</th><th></th></tr></thead><tbody id="records"></tbody></table></div><div class="hint">MX example: 10 mail.home.arpa. PTR name: 10.50.168.192.in-addr.arpa. Use fully qualified names for CNAME targets.</div></div>
</section>
<section class="panel" id="tab-dhcp" hidden>
 <div class="card"><h2>DHCP settings</h2><div class="grid">
  <div class="field"><label for="pool_start">Pool start</label><input id="pool_start" placeholder="192.168.50.100"></div>
  <div class="field"><label for="pool_end">Pool end</label><input id="pool_end" placeholder="192.168.50.200"></div>
  <div class="field"><label for="lease_seconds">Lease duration (seconds)</label><input id="lease_seconds" type="number" min="120" max="2592000"></div>
  <div class="field"><label for="router">Gateway / router (optional)</label><input id="router" placeholder="Leave empty to omit the gateway"></div>
  <div class="field"><label for="dhcp_dns">Client DNS servers (comma-separated)</label><input id="dhcp_dns" placeholder="192.168.50.1"></div>
  <div class="field"><label for="dhcp_domain">Domain (optional)</label><input id="dhcp_domain" placeholder="home.arpa"></div>
 </div><div class="notice">For an isolated local network, leave the gateway empty. This tool provides DNS and DHCP; internet sharing, NAT, and Wi-Fi access point services are configured separately.</div><p class="hint">Server, gateway, and advertised DNS addresses are excluded from the dynamic pool. Keep other static devices outside the pool or add a reservation.</p></div>
 <div class="card"><div class="section-head"><div><h2>Address reservations</h2><div class="hint">Assign a fixed address to a MAC address, inside or outside the pool in the same subnet.</div></div><button id="addReservation">+ Add reservation</button></div><div class="table-wrap"><table><thead><tr><th>MAC address</th><th>IP address</th><th></th></tr></thead><tbody id="reservations"></tbody></table></div></div>
 <div class="card"><div class="section-head"><div><h2>Custom DHCP options</h2><div class="hint">Deliver extra settings, such as option 42 / ipv4 for NTP or option 66 / text for a TFTP server.</div></div><button id="addOption">+ Add option</button></div><div class="table-wrap"><table><thead><tr><th>Code</th><th>Data type</th><th>Value</th><th></th></tr></thead><tbody id="options"></tbody></table></div><p class="hint">ipv4: comma-separated addresses. hex: raw bytes, such as 01 ff 20. Core options use the dedicated fields above.</p></div>
</section>
<section class="panel" id="tab-leases" hidden><div class="card"><h2>Active DHCP leases</h2><p class="hint">Updates automatically. Confirmed leases persist across restarts.</p><div class="table-wrap"><table><thead><tr><th>IP address</th><th>MAC address</th><th>Hostname</th><th>Time remaining</th><th>Expires</th></tr></thead><tbody id="leases"></tbody></table></div><div id="noLeases" class="empty">No active leases yet. Start DHCP to see client allocations here.</div></div></section>
<section class="panel" id="tab-logs" hidden><div class="card"><div class="section-head"><div><h2>Activity log</h2><div class="hint">Follow DNS queries, DHCP allocations, upstream errors, and service events.</div></div><span id="logStatus" class="badge on">Live · updates every second</span></div><div class="log-controls"><select id="logService" aria-label="Filter by service"><option value="">All services</option><option>DNS</option><option>DHCP</option><option>SYSTEM</option></select><input id="logSearch" placeholder="Search events…" aria-label="Search events"><button id="pauseLog">Pause</button><button id="downloadLog">Export log</button></div><div id="log" class="log" role="log" aria-live="off"></div><p class="hint">The latest 2,000 events are held in memory. Export the log to keep a copy.</p></div></section>
<div class="buttons"><button id="exportConfig">Export configuration</button><label class="file-button" for="importConfig">Import configuration</label><input type="file" id="importConfig" accept=".json,application/json" hidden></div>
<p class="foot">Stop services before saving changes, then start the services you need. This console is available only on this computer. Press Ctrl+C in the terminal to quit.</p>
</main>
<script>
"use strict";
const TOKEN="__ADMIN_TOKEN__";
const $=id=>document.getElementById(id);
let config=null,state={},nicList=[],dirty=false,busy=false,cursor=0,events=[],paused=false,polling=false;
const list=s=>s.split(/[\n,]+/).map(x=>x.trim()).filter(Boolean);
function message(text,error=false){$("message").textContent=text;$("message").classList.toggle("error",error);$("message").hidden=false;}
function markDirty(){dirty=true;$("dirty").hidden=false;updateButtons();}
function clean(){dirty=false;$("dirty").hidden=true;updateButtons();}
async function api(path,body){const res=await fetch(path,{method:body?"POST":"GET",headers:{"X-Admin-Token":TOKEN,...(body?{"Content-Type":"application/json"}:{})},body:body?JSON.stringify(body):undefined});const data=await res.json();if(!res.ok)throw new Error(data.error||"Request failed");return data;}
function updateButtons(){for(const service of ["dns","dhcp"]){const running=!!state[service+"_running"];const badge=$(service+"Badge");badge.textContent=running?"Running":"Stopped";badge.classList.toggle("on",running);const button=$(service+"Toggle");button.textContent=(running?"Stop ":"Start ")+service.toUpperCase();button.classList.toggle("stop",running);button.disabled=busy||(!running&&(dirty||(service==="dhcp"&&!state.dhcp_supported)));}$("save").disabled=busy||state.dns_running||state.dhcp_running;$("stopAll").disabled=busy||(!state.dns_running&&!state.dhcp_running);}
function nicOptions(){const current=config?config.interface+"|"+config.bind_ip:"";$("iface").replaceChildren(new Option("Select an interface…",""));nicList.forEach((nic,index)=>{const opt=new Option(`${nic.name} · ${nic.ip}${nic.up?"":" (inactive)"}`,String(index));opt.disabled=!nic.up;$("iface").add(opt);if(nic.name+"|"+nic.ip===current)$("iface").value=String(index);});}
const schemas={records:[{key:"name",placeholder:"printer.home.arpa"},{key:"type",options:["A","AAAA","CNAME","TXT","MX","PTR"]},{key:"value",placeholder:"192.168.50.10"},{key:"ttl",type:"number"}],reservations:[{key:"mac",placeholder:"aa:bb:cc:dd:ee:ff"},{key:"ip",placeholder:"192.168.50.10"}],options:[{key:"code",type:"number"},{key:"type",options:["text","ipv4","hex","uint8","uint16","uint32"]},{key:"value",placeholder:"Option value"}]};
function row(table,data){const tr=document.createElement("tr");for(const field of schemas[table]){const td=document.createElement("td");const input=document.createElement(field.options?"select":"input");if(field.options)for(const value of field.options)input.add(new Option(value,value));else{input.type=field.type||"text";input.placeholder=field.placeholder||"";}input.dataset.key=field.key;input.setAttribute("aria-label",field.key);input.value=data[field.key]??"";input.addEventListener("input",markDirty);td.append(input);tr.append(td);}const td=document.createElement("td");const button=document.createElement("button");button.className="remove";button.textContent="Remove";button.addEventListener("click",()=>{tr.remove();markDirty();});td.append(button);tr.append(td);$(table).append(tr);}
function rows(table){return [...$(table).rows].map(tr=>Object.fromEntries([...tr.querySelectorAll("[data-key]")].map(el=>[el.dataset.key,el.type==="number"?Number(el.value):el.value.trim()])));}
function populate(c){config=structuredClone(c);$("bind_ip").value=c.bind_ip;$("netmask").value=c.netmask;$("dns_port").value=c.dns.port;$("dns_timeout").value=c.dns.timeout;$("local_zone").value=c.dns.local_zone;$("forwarders").value=c.dns.forwarders.join("\n");for(const key of ["pool_start","pool_end","lease_seconds","router"])$(key).value=c.dhcp[key];$("dhcp_dns").value=c.dhcp.dns_servers.join(", ");$("dhcp_domain").value=c.dhcp.domain;for(const key of Object.keys(schemas)){$(key).replaceChildren();(key==="records"?c.dns.records:c.dhcp[key]).forEach(item=>row(key,item));}nicOptions();}
function collect(){const c=structuredClone(config);const nic=nicList[Number($("iface").value)];if($("iface").value===""||!nic)throw new Error("Select an active network interface.");c.interface=nic.name;c.bind_ip=$("bind_ip").value;c.netmask=$("netmask").value;c.dns={port:Number($("dns_port").value),timeout:Number($("dns_timeout").value),local_zone:$("local_zone").value.trim(),forwarders:list($("forwarders").value),records:rows("records")};c.dhcp={pool_start:$("pool_start").value.trim(),pool_end:$("pool_end").value.trim(),lease_seconds:Number($("lease_seconds").value),router:$("router").value.trim(),dns_servers:list($("dhcp_dns").value),domain:$("dhcp_domain").value.trim(),reservations:rows("reservations"),options:rows("options")};return c;}
function ipnum(ip){return ip.split(".").reduce((n,x)=>(n*256+Number(x))>>>0,0);}
function ipstr(n){return [24,16,8,0].map(b=>(n>>>b)&255).join(".");}
$("iface").addEventListener("change",()=>{if(!$("iface").value)return;const nic=nicList[Number($("iface").value)];const previous=$("bind_ip").value;$("bind_ip").value=nic.ip;$("netmask").value=nic.netmask;config.interface=nic.name;config.bind_ip=nic.ip;const mask=ipnum(nic.netmask),net=(ipnum(nic.ip)&mask)>>>0,broadcast=(net|(~mask>>>0))>>>0;const max=broadcast-1;$("pool_start").value=ipstr(Math.min(net+100,max));$("pool_end").value=ipstr(Math.min(net+200,max));if($("dhcp_dns").value.trim()===previous)$("dhcp_dns").value=nic.ip;$("router").value="";markDirty();});
for(const input of document.querySelectorAll("input:not([readonly]):not([type=file]),textarea,select:not(#iface)"))if(!["logService","logSearch"].includes(input.id))input.addEventListener("input",markDirty);
$("addRecord").onclick=()=>{row("records",{name:"",type:"A",value:"",ttl:300});markDirty();};
$("addReservation").onclick=()=>{row("reservations",{mac:"",ip:""});markDirty();};
$("addOption").onclick=()=>{row("options",{code:42,type:"ipv4",value:""});markDirty();};
async function action(name){if(busy)return;busy=true;updateButtons();try{await api("/api/action",{action:name});await refreshState();message(name.startsWith("start")?"Service started.":"Service stopped.");}catch(err){message(err.message,true);}finally{busy=false;updateButtons();}}
$("dnsToggle").onclick=()=>action(state.dns_running?"stop_dns":"start_dns");$("dhcpToggle").onclick=()=>action(state.dhcp_running?"stop_dhcp":"start_dhcp");
$("stopAll").onclick=async()=>{await action("stop_dhcp");await action("stop_dns");};
$("save").onclick=async()=>{if(busy)return;busy=true;updateButtons();try{const result=await api("/api/action",{action:"save",config:collect()});populate(result.config);clean();message("Configuration saved. You can now start the services you need.");await refreshState();}catch(err){message(err.message,true);}finally{busy=false;updateButtons();}};
for(const button of document.querySelectorAll("[data-tab]"))button.onclick=()=>{for(const tab of document.querySelectorAll("[data-tab]")){const selected=tab===button;tab.classList.toggle("active",selected);tab.setAttribute("aria-selected",String(selected));$("tab-"+tab.dataset.tab).hidden=!selected;}if(button.dataset.tab==="logs")renderLog();};
function renderLeases(){const tbody=$("leases");tbody.replaceChildren();for(const lease of state.leases){const tr=document.createElement("tr");for(const value of [lease.ip,lease.mac,lease.hostname||"—",`${Math.floor(lease.remaining/60)} min ${lease.remaining%60} s`,new Date(lease.expires_at).toLocaleString("en-GB")]){const td=document.createElement("td");td.textContent=value;tr.append(td);}tbody.append(tr);}$("leaseCount").textContent=state.leases.length;$("noLeases").hidden=!!state.leases.length;}
async function refreshState(){state=await api("/api/state");nicList=state.interfaces;$("platformNote").hidden=state.dhcp_supported;$("dnsInfo").textContent=`UDP + TCP · ${config.bind_ip}:${config.dns.port}`;$("dhcpInfo").textContent=`UDP 67 / 68 · ${state.leases.length} active leases`;$("dnsWarning").hidden=!(state.dhcp_running&&!state.dns_running&&config.dhcp.dns_servers.includes(config.bind_ip));renderLeases();updateButtons();}
$("refreshInterfaces").onclick=async()=>{try{if(dirty){message("Save your changes or reload the page before refreshing the interfaces.",true);return;}await refreshState();nicOptions();message("Interfaces refreshed.");}catch(err){message(err.message,true);}};
function renderLog(){if(paused)return;const service=$("logService").value,search=$("logSearch").value.toLowerCase();const box=$("log");const bottom=box.scrollTop+box.clientHeight>=box.scrollHeight-45;const visible=events.filter(e=>(!service||e.service===service)&&(!search||e.message.toLowerCase().includes(search)));const fragment=document.createDocumentFragment();for(const e of visible){const line=document.createElement("div");line.className="log-line "+e.level.toLowerCase();line.textContent=`${new Date(e.time).toLocaleTimeString("en-GB")}  ${e.service.padEnd(6)} ${e.level.padEnd(5)} ${e.message}`;fragment.append(line);}box.replaceChildren(fragment);if(bottom)box.scrollTop=box.scrollHeight;}
$("logService").onchange=renderLog;$("logSearch").oninput=renderLog;$("pauseLog").onclick=()=>{paused=!paused;$("pauseLog").textContent=paused?"Resume":"Pause";$("logStatus").textContent=paused?"View paused":"Live · updates every second";$("logStatus").classList.toggle("on",!paused);renderLog();};
function download(name,data,type){const url=URL.createObjectURL(new Blob([data],{type}));const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$("downloadLog").onclick=()=>download("lan-dns-dhcp.log",events.map(e=>`${e.time} [${e.service}] ${e.level} ${e.message}`).join("\n"),"text/plain;charset=utf-8");
$("exportConfig").onclick=()=>{try{download("lan-config.json",JSON.stringify(collect(),null,2),"application/json");}catch(err){message(err.message,true);}};
$("importConfig").onchange=async event=>{try{const file=event.target.files[0];if(!file)return;if(file.size>262144)throw new Error("Configuration file is too large.");const c=JSON.parse(await file.text());if(!c.dns||!c.dhcp||!Array.isArray(c.dns.records)||!Array.isArray(c.dhcp.options)||!Array.isArray(c.dhcp.reservations))throw new Error("Invalid configuration format.");populate(c);markDirty();message("Configuration loaded. Save to validate and apply it.");}catch(err){message(err.message,true);}finally{event.target.value="";}};
window.addEventListener("beforeunload",event=>{if(dirty){event.preventDefault();event.returnValue="";}});
async function poll(){if(polling)return;polling=true;try{await refreshState();const result=await api("/api/logs?after="+cursor);if(result.cursor<cursor)events=[];cursor=result.cursor;events.push(...result.events);events=events.slice(-2000);renderLog();if(!paused){$("logStatus").textContent="Live · updates every second";$("logStatus").classList.add("on");}}catch(err){$("logStatus").textContent="Connection lost";$("logStatus").classList.remove("on");}finally{polling=false;}}
(async()=>{try{const [c,s]=await Promise.all([api("/api/config"),api("/api/state")]);state=s;nicList=s.interfaces;populate(c);clean();await poll();setInterval(poll,1000);}catch(err){message(err.message,true);}})();
</script>
</body>
</html>
"""



# ==========================================================================
# INTERFACES
# ==========================================================================

import ctypes as C
import ipaddress
import socket
import sys


def interfaces():
    return windows_interfaces() if sys.platform == "win32" else posix_interfaces()


def windows_interfaces():
    u32 = C.c_uint32

    class SocketAddress(C.Structure):
        _fields_ = [("address", C.c_void_p), ("length", C.c_int)]

    class Unicast(C.Structure):
        pass

    Unicast._fields_ = [("alignment", C.c_uint64), ("next", C.POINTER(Unicast)),
                       ("socket", SocketAddress), ("prefix_origin", u32), ("suffix_origin", u32),
                       ("dad_state", u32), ("valid_lifetime", u32), ("preferred_lifetime", u32),
                       ("lease_lifetime", u32), ("prefix_length", C.c_ubyte)]

    class Adapter(C.Structure):
        pass

    Adapter._fields_ = [("alignment", C.c_uint64), ("next", C.POINTER(Adapter)),
                       ("adapter_name", C.c_char_p), ("unicast", C.POINTER(Unicast)),
                       ("anycast", C.c_void_p), ("multicast", C.c_void_p), ("dns", C.c_void_p),
                       ("dns_suffix", C.c_wchar_p), ("description", C.c_wchar_p),
                       ("friendly_name", C.c_wchar_p), ("physical_address", C.c_ubyte * 8),
                       ("physical_length", u32), ("flags", u32), ("mtu", u32),
                       ("if_type", u32), ("oper_status", u32)]
    api = C.WinDLL("iphlpapi.dll").GetAdaptersAddresses
    api.argtypes = [u32, u32, C.c_void_p, C.c_void_p, C.POINTER(u32)]
    api.restype = u32
    size = u32(16384)
    for _ in range(4):
        if size.value > 2 * 1024 * 1024:
            raise OSError("Adapter enumeration exceeded the buffer limit.")
        buffer = C.create_string_buffer(size.value)
        result = api(socket.AF_INET, 2 | 4 | 8, None, buffer, C.byref(size))
        if result == 111:  # ERROR_BUFFER_OVERFLOW: OS supplies the required size.
            continue
        if result == 232:  # ERROR_NO_DATA
            return []
        if result:
            raise OSError(result, "Windows adapter enumeration failed.")
        break
    else:
        raise OSError("Windows adapter list changed repeatedly; refresh and retry.")
    adapters, seen = [], set()
    current = C.cast(buffer, C.POINTER(Adapter))
    while current:
        adapter = current.contents
        name = adapter.friendly_name or adapter.adapter_name.decode("utf-8", "replace")
        address = adapter.unicast
        while address:
            entry = address.contents
            if entry.socket.address and entry.socket.length >= 8:
                raw = C.string_at(entry.socket.address, 8)
                if int.from_bytes(raw[:2], sys.byteorder) == socket.AF_INET and entry.prefix_length <= 32:
                    ip = socket.inet_ntoa(raw[4:8])
                    if (name, ip) not in seen:
                        adapters.append({"name": name, "ip": ip,
                                         "netmask": str(ipaddress.IPv4Network(f"0.0.0.0/{entry.prefix_length}").netmask),
                                         "up": adapter.oper_status == 1})
                        seen.add((name, ip))
            address = entry.next
        current = adapter.next
    return adapters


def posix_interfaces():
    class IfAddress(C.Structure):
        pass

    IfAddress._fields_ = [("next", C.POINTER(IfAddress)), ("name", C.c_char_p),
                         ("flags", C.c_uint), ("address", C.c_void_p),
                         ("netmask", C.c_void_p), ("destination", C.c_void_p), ("data", C.c_void_p)]
    libc = C.CDLL(None, use_errno=True)
    getifaddrs = libc.getifaddrs
    getifaddrs.argtypes = [C.POINTER(C.POINTER(IfAddress))]
    getifaddrs.restype = C.c_int
    freeifaddrs = libc.freeifaddrs
    freeifaddrs.argtypes = [C.POINTER(IfAddress)]
    freeifaddrs.restype = None
    head = C.POINTER(IfAddress)()
    if getifaddrs(C.byref(head)) != 0:
        raise OSError(C.get_errno(), "Could not enumerate network interfaces.")
    result, seen = [], set()
    try:
        current = head
        while current:
            entry = current.contents
            if entry.address:
                raw = C.string_at(entry.address, 8)
                family = raw[1] if sys.platform == "darwin" else int.from_bytes(raw[:2], sys.byteorder)
                if family == socket.AF_INET:
                    name = entry.name.decode("utf-8", "replace")
                    ip = socket.inet_ntoa(raw[4:8])
                    mask = socket.inet_ntoa(C.string_at(entry.netmask, 8)[4:8]) if entry.netmask else "255.255.255.255"
                    if (name, ip) not in seen:
                        result.append({"name": name, "ip": ip, "netmask": mask, "up": bool(entry.flags & 1)})
                        seen.add((name, ip))
            current = entry.next
    finally:
        freeifaddrs(head)
    return result


# ==========================================================================
# DNSWIRE
# ==========================================================================

import ipaddress
import secrets
import socket
import struct


class Codes:
    def __init__(self, prefix, **values):
        self.prefix = prefix
        self.names = {value: name for name, value in values.items()}
        self.__dict__.update(values)

    def __getitem__(self, code):
        return self.names.get(code, f"{self.prefix}{code}")

    def number(self, value):
        if isinstance(value, int):
            return value
        value = value.upper()
        return getattr(self, value) if value in self.__dict__ else int(value.removeprefix(self.prefix))


QTYPE = Codes("TYPE", A=1, NS=2, CNAME=5, SOA=6, PTR=12, MX=15, TXT=16, AAAA=28, SRV=33, OPT=41, ANY=255)
RCODE = Codes("RCODE", NOERROR=0, FORMERR=1, SERVFAIL=2, NXDOMAIN=3, NOTIMP=4, REFUSED=5)


class DNSLabel:
    def __init__(self, value):
        if isinstance(value, DNSLabel):
            self.labels = value.labels
        elif isinstance(value, tuple):
            self.labels = value
        else:
            value = str(value).rstrip(".")
            self.labels = tuple(x.encode("idna") for x in value.split(".")) if value else ()
        if any(not 1 <= len(x) <= 63 for x in self.labels) or sum(len(x) + 1 for x in self.labels) + 1 > 255:
            raise ValueError("Invalid DNS name length.")

    def pack(self):
        return b"".join(bytes([len(label)]) + label for label in self.labels) + b"\0"

    def __str__(self):
        def escaped(label):
            return "".join(chr(x) if 33 <= x <= 126 and x not in (46, 92) else f"\\{x:03d}" for x in label)
        return ".".join(escaped(x) for x in self.labels) + "."

    def __eq__(self, other):
        return isinstance(other, DNSLabel) and tuple(x.lower() for x in self.labels) == tuple(x.lower() for x in other.labels)


def read_name(data, offset):
    labels, seen = [], set()
    end, total = None, 1
    while True:
        if offset >= len(data) or offset in seen or len(seen) > 128:
            raise ValueError("Invalid or cyclic DNS name compression.")
        seen.add(offset)
        length = data[offset]
        if length & 0xC0 == 0xC0:
            if offset + 1 >= len(data):
                raise ValueError("Truncated DNS name pointer.")
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            if pointer >= offset:
                raise ValueError("DNS compression pointer must refer to an earlier name.")
            if end is None:
                end = offset + 2
            offset = pointer
            continue
        if length & 0xC0 or length > 63:
            raise ValueError("Invalid DNS label.")
        offset += 1
        if not length:
            return DNSLabel(tuple(labels)), end if end is not None else offset
        if offset + length > len(data):
            raise ValueError("Truncated DNS label.")
        labels.append(data[offset:offset + length])
        total += length + 1
        if total > 255:
            raise ValueError("DNS name exceeds 255 bytes.")
        offset += length


class DNSHeader:
    def __init__(self, id=None, flags=0x0100, **fields):
        self.id = secrets.randbits(16) if id is None else id
        for name, shift, mask in self.bits():
            setattr(self, name, (flags >> shift) & mask)
        self.__dict__.update(fields)

    @staticmethod
    def bits():
        return [("qr",15,1),("opcode",11,15),("aa",10,1),("tc",9,1),("rd",8,1),
                ("ra",7,1),("z",6,1),("ad",5,1),("cd",4,1),("rcode",0,15)]

    def pack(self, counts):
        flags = sum((int(getattr(self, name)) & mask) << shift for name, shift, mask in self.bits())
        return struct.pack("!6H", self.id, flags, *counts)


class DNSQuestion:
    def __init__(self, name, qtype=1, qclass=1):
        self.qname, self.qtype, self.qclass = DNSLabel(name), qtype, qclass

    def pack(self):
        return self.qname.pack() + struct.pack("!HH", self.qtype, self.qclass)

    def __eq__(self, other):
        return isinstance(other, DNSQuestion) and self.qname == other.qname and self.qtype == other.qtype and self.qclass == other.qclass

    def __str__(self):
        return f"{self.qname} {QTYPE[self.qtype]}"


class A:
    def __init__(self, value):
        self.value = ipaddress.IPv4Address(value)

    def pack(self):
        return self.value.packed

    def __str__(self):
        return str(self.value)


class AAAA(A):
    def __init__(self, value):
        self.value = ipaddress.IPv6Address(value)


class CNAME:
    def __init__(self, value):
        self.label = DNSLabel(value)

    def pack(self):
        return self.label.pack()

    def __str__(self):
        return str(self.label)


class PTR(CNAME):
    pass


class MX(CNAME):
    def __init__(self, value, preference=10):
        super().__init__(value)
        self.preference = preference

    def pack(self):
        return struct.pack("!H", self.preference) + super().pack()

    def __str__(self):
        return f"{self.preference} {self.label}"


class TXT:
    def __init__(self, values):
        self.data = [x.encode("utf-8") if isinstance(x,str) else bytes(x) for x in values]
        if any(len(x) > 255 for x in self.data):
            raise ValueError("Each TXT segment must fit in 255 bytes.")

    def pack(self):
        return b"".join(bytes([len(x)]) + x for x in self.data)

    def __str__(self):
        return b"".join(self.data).decode("utf-8", "backslashreplace")


class Opaque:
    def __init__(self, data):
        self.data = bytes(data)

    def pack(self):
        return self.data


class RR:
    def __init__(self, name, rtype=1, rclass=1, ttl=0, rdata=None):
        self.rname, self.rtype, self.rclass = DNSLabel(name), rtype, rclass
        self.ttl, self.rdata = ttl, rdata or Opaque(b"")

    def pack(self):
        data = self.rdata.pack()
        return self.rname.pack() + struct.pack("!HHIH", self.rtype, self.rclass, self.ttl, len(data)) + data


def parse_rr(data, offset):
    name, offset = read_name(data, offset)
    if offset + 10 > len(data):
        raise ValueError("Truncated DNS record header.")
    kind, cls, ttl, length = struct.unpack_from("!HHIH", data, offset)
    offset += 10
    end = offset + length
    if end > len(data):
        raise ValueError("Truncated DNS record data.")
    raw = data[offset:end]
    if (kind == QTYPE.A and length != 4) or (kind == QTYPE.AAAA and length != 16):
        raise ValueError("Invalid address record length.")
    value = Opaque(raw)
    if kind == QTYPE.A and length == 4:
        value = A(raw)
    elif kind == QTYPE.AAAA and length == 16:
        value = AAAA(raw)
    elif kind in (QTYPE.CNAME,QTYPE.PTR,QTYPE.NS):
        target, consumed = read_name(data,offset)
        if consumed != end:
            raise ValueError("Invalid DNS name record length.")
        value = PTR(target) if kind == QTYPE.PTR else CNAME(target)
    elif kind == QTYPE.MX:
        if length < 3:
            raise ValueError("Truncated MX record.")
        target, consumed = read_name(data,offset+2)
        if consumed != end:
            raise ValueError("Invalid MX record length.")
        value = MX(target,struct.unpack_from("!H",data,offset)[0])
    elif kind == QTYPE.TXT:
        segments = []
        position = offset
        while position < end:
            count = data[position]
            position += 1
            if position + count > end:
                raise ValueError("Truncated TXT segment.")
            segments.append(data[position:position+count])
            position += count
        value = TXT(segments)
    return RR(name,kind,cls,ttl,value), end


class DNSRecord:
    def __init__(self, header=None, q=None):
        self.header = header or DNSHeader()
        self.questions = [q] if q else []
        self.rr, self.auth, self.ar = [], [], []
        self.original = None

    @property
    def q(self):
        return self.questions[0] if self.questions else DNSQuestion("")

    @classmethod
    def question(cls, name, kind="A"):
        return cls(q=DNSQuestion(name,QTYPE.number(kind)))

    @classmethod
    def parse(cls, packet):
        data = bytes(packet)
        if not 12 <= len(data) <= 65535:
            raise ValueError("Invalid DNS packet length.")
        ident, flags, nq, na, ns, nr = struct.unpack_from("!6H",data)
        if nq > 16 or na + ns + nr > 2048:
            raise ValueError("DNS packet has too many entries.")
        result = cls(DNSHeader(ident,flags))
        offset = 12
        for _ in range(nq):
            name, offset = read_name(data,offset)
            if offset + 4 > len(data):
                raise ValueError("Truncated DNS question.")
            kind, group = struct.unpack_from("!HH",data,offset)
            result.questions.append(DNSQuestion(name,kind,group))
            offset += 4
        for count, section in ((na,result.rr),(ns,result.auth),(nr,result.ar)):
            for _ in range(count):
                rr, offset = parse_rr(data,offset)
                section.append(rr)
        if offset != len(data):
            raise ValueError("Unexpected bytes after DNS message.")
        result.original = data
        return result

    def reply(self, aa=1, ra=1):
        reply = DNSRecord(DNSHeader(self.header.id,qr=1,opcode=self.header.opcode,
                                    aa=aa,ra=ra,rd=self.header.rd,cd=self.header.cd))
        reply.questions = list(self.questions)
        return reply

    def add_answer(self, *answers):
        self.original = None
        self.rr.extend(answers)

    def pack(self):
        header = self.header.pack((len(self.questions),len(self.rr),len(self.auth),len(self.ar)))
        if self.original is not None:
            return header + self.original[12:]
        return header + b"".join(x.pack() for x in [*self.questions,*self.rr,*self.auth,*self.ar])

    def send(self, address, port=53, tcp=False, timeout=2):
        family = socket.AF_INET6 if ":" in address else socket.AF_INET
        with socket.socket(family,socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.connect((address,port))
            packet = self.pack()
            if not tcp:
                sock.send(packet)
                return sock.recv(65535)
            sock.sendall(struct.pack("!H",len(packet))+packet)
            def read(length):
                chunks = bytearray()
                while len(chunks) < length:
                    chunk = sock.recv(length-len(chunks))
                    if not chunk:
                        raise ConnectionError("Truncated DNS TCP response.")
                    chunks.extend(chunk)
                return bytes(chunks)
            return read(struct.unpack("!H",read(2))[0])


# ==========================================================================
# COMMON
# ==========================================================================

import copy
import ipaddress
import json
import os
import re
import socket
import struct
import threading
from collections import deque
from datetime import datetime, timezone
from pathlib import Path


DEFAULTS = {
    "interface": "", "bind_ip": "192.168.50.1", "netmask": "255.255.255.0",
    "dns": {"port": 53, "forwarders": ["1.1.1.1", "9.9.9.9"],
            "timeout": 2.0, "local_zone": "home.arpa", "records": []},
    "dhcp": {"pool_start": "192.168.50.100", "pool_end": "192.168.50.200",
             "lease_seconds": 3600, "router": "", "dns_servers": ["192.168.50.1"],
             "domain": "home.arpa", "reservations": [], "options": []},
}


class EventLog:
    def __init__(self):
        self.lock = threading.Lock()
        self.items = deque(maxlen=2000)
        self.seq = 0

    def add(self, service, message, level="INFO"):
        with self.lock:
            self.seq += 1
            item = {"id": self.seq, "time": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "service": service, "level": level, "message": str(message)[:2000]}
            self.items.append(item)

    def since(self, cursor=0):
        with self.lock:
            return {"cursor": self.seq, "events": [x for x in self.items if x["id"] > cursor]}


def check_interface(config):
    if not any(x["name"] == config["interface"] and x["ip"] == config["bind_ip"] and x["up"]
               for x in interfaces()):
        raise ValueError("The selected interface is inactive or does not have this IPv4 address. "
                         "Assign a static IP in your system settings first, then refresh the interfaces.")


def windows_interface_index(interface):
    """Resolve Python's technical names and Windows adapter aliases."""
    try:
        return socket.if_nametoindex(interface)
    except OSError:
        import ctypes
        api = ctypes.WinDLL("iphlpapi.dll")
        alias_to_luid = api.ConvertInterfaceAliasToLuid
        alias_to_luid.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint64)]
        alias_to_luid.restype = ctypes.c_uint32
        luid_to_index = api.ConvertInterfaceLuidToIndex
        luid_to_index.argtypes = [ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint32)]
        luid_to_index.restype = ctypes.c_uint32
        luid, index = ctypes.c_uint64(), ctypes.c_uint32()
        error = alias_to_luid(interface, ctypes.byref(luid))
        if not error:
            error = luid_to_index(ctypes.byref(luid), ctypes.byref(index))
        if error or not index.value:
            raise OSError(error, f"Windows interface not found: {interface}")
        return index.value


def bind_device(sock, interface):
    """Restrict incoming AND outgoing DHCP traffic to the selected interface."""
    import sys
    if sys.platform == "darwin":
        sock.setsockopt(socket.IPPROTO_IP, getattr(socket, "IP_BOUND_IF", 25),
                        socket.if_nametoindex(interface))
    elif sys.platform.startswith("linux"):
        sock.setsockopt(socket.SOL_SOCKET, getattr(socket, "SO_BINDTODEVICE", 25),
                        interface.encode() + b"\0")
    elif sys.platform == "win32":
        index = windows_interface_index(interface)
        try:
            # Windows SDK: IP_IFLIST=28, IP_ADD_IFLIST=29, IP_UNICAST_IF=31.
            # The receive allow-list is enabled empty first (fail closed).
            # IF_INDEX in the allow-list is native order; IP_UNICAST_IF is network order.
            sock.setsockopt(socket.IPPROTO_IP, 28, 1)
            sock.setsockopt(socket.IPPROTO_IP, 29, struct.pack("=I", index))
            sock.setsockopt(socket.IPPROTO_IP, 31, struct.pack("!I", index))
            sock.setsockopt(socket.IPPROTO_IP, 22, 1)  # IP_RECEIVE_BROADCAST
        except OSError as exc:
            raise OSError(exc.errno, "Windows interface binding failed. "
                          "DHCP requires Windows 10 version 1803 or later, or Windows 11. "
                          "DHCP will not start without interface isolation.") from exc
    else:
        raise ValueError("DHCP is supported on Windows, macOS, and Linux.")


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def ipv4(value):
    return str(ipaddress.IPv4Address(str(value).strip()))


def domain(value, wildcard=False):
    value = str(value).strip().rstrip(".")
    if not value:
        raise ValueError("DNS name must not be empty.")
    labels = value.split(".")
    output = []
    for i, label in enumerate(labels):
        if wildcard and i == 0 and label == "*":
            output.append("*")
            continue
        label = label.encode("idna").decode("ascii").lower()
        if not 1 <= len(label) <= 63 or not re.fullmatch(r"[a-z0-9_](?:[a-z0-9_-]*[a-z0-9_])?", label):
            raise ValueError("Invalid DNS name.")
        output.append(label)
    result = ".".join(output)
    if len(result) > 253:
        raise ValueError("DNS name is too long.")
    return result


def endpoint(value):
    value = str(value).strip()
    if value.startswith("["):
        match = re.fullmatch(r"\[([^]]+)\](?::(\d+))?", value)
        if not match:
            raise ValueError("Enter a forwarder such as 1.1.1.1 or [2606:4700:4700::1111]:53.")
        host, port = match[1], int(match[2] or 53)
    elif value.count(":") == 1:
        host, port = value.rsplit(":", 1)
        port = int(port)
    else:
        host, port = value, 53
    host = str(ipaddress.ip_address(host))
    if not 1 <= port <= 65535:
        raise ValueError("Forwarder port must be between 1 and 65535.")
    return host, port


def rdata(record):
    value, kind = record["value"], record["type"]
    if kind == "A":
        return A(str(ipaddress.IPv4Address(value)))
    if kind == "AAAA":
        return AAAA(str(ipaddress.IPv6Address(value)))
    if kind == "CNAME":
        return CNAME(DNSLabel(domain(value)))
    if kind == "PTR":
        return PTR(DNSLabel(domain(value)))
    if kind == "TXT":
        raw = value.encode("utf-8")
        if len(raw) > 1024:
            raise ValueError("TXT record: maximum 1024 UTF-8 bytes.")
        return TXT([raw[i:i + 255] for i in range(0, len(raw), 255)] or [b""])
    if kind == "MX":
        priority, host = value.split(None, 1)
        priority = int(priority)
        if not 0 <= priority <= 65535:
            raise ValueError("MX priority must be between 0 and 65535.")
        return MX(domain(host), priority)
    raise ValueError("DNS type must be A, AAAA, CNAME, PTR, TXT, or MX.")


def mac(value):
    value = str(value).lower().replace("-", ":").strip()
    if not re.fullmatch(r"(?:[0-9a-f]{2}:){5}[0-9a-f]{2}", value):
        raise ValueError("Enter a MAC address in aa:bb:cc:dd:ee:ff format.")
    return value


def option_value(item):
    kind, value = item["type"], str(item["value"])
    if kind == "text":
        result = value.encode("utf-8")
    elif kind == "hex":
        result = bytes.fromhex(value)
    elif kind == "ipv4":
        result = b"".join(socket.inet_aton(ipv4(x)) for x in value.split(","))
    elif kind in ("uint8", "uint16", "uint32"):
        result = struct.pack({"uint8": "!B", "uint16": "!H", "uint32": "!I"}[kind], int(value))
    else:
        raise ValueError("DHCP option type must be text, hex, ipv4, uint8, uint16, or uint32.")
    if not 1 <= len(result) <= 255:
        raise ValueError("DHCP option values must contain 1–255 bytes.")
    return result


def validate(raw):
    """Full validation before changing configuration or opening network ports."""
    if not isinstance(raw, dict):
        raise ValueError("Configuration must be a JSON object.")
    c = copy.deepcopy(raw)
    c["interface"] = str(c["interface"]).strip()
    c["bind_ip"] = ipv4(c["bind_ip"])
    network = ipaddress.IPv4Network(f'{c["bind_ip"]}/{c["netmask"]}', strict=False)
    c["netmask"] = str(network.netmask)
    if network.prefixlen > 30 or ipaddress.IPv4Address(c["bind_ip"]) in (network.network_address, network.broadcast_address):
        raise ValueError("Server IP must be a host address in a network with at least four addresses.")
    d = c["dns"]
    d["port"] = int(d["port"])
    d["timeout"] = float(d["timeout"])
    if not 1 <= d["port"] <= 65535 or not 0.2 <= d["timeout"] <= 5:
        raise ValueError("Choose a DNS port between 1 and 65535 and a forwarder timeout between 0.2 and 5 seconds.")
    if len(d["forwarders"]) > 4:
        raise ValueError("A maximum of four DNS forwarders is supported.")
    for f in d["forwarders"]:
        host, port = endpoint(f)
        local_ips = {x["ip"] for x in interfaces()} | {c["bind_ip"], "127.0.0.1", "::1"}
        if host in local_ips and port == d["port"]:
            raise ValueError("The DNS server cannot forward to itself (forwarding loop).")
    d["local_zone"] = domain(d["local_zone"]) if str(d["local_zone"]).strip() else ""
    if len(d["records"]) > 1000:
        raise ValueError("A maximum of 1000 DNS records is supported.")
    kinds = {}
    for r in d["records"]:
        r["name"] = domain(r["name"], wildcard=True)
        r["type"] = str(r["type"]).upper()
        r["value"] = str(r["value"])
        r["ttl"] = int(r["ttl"])
        if not 0 <= r["ttl"] <= 2147483647:
            raise ValueError("TTL must be between 0 and 2147483647.")
        rdata(r)
        kinds.setdefault(r["name"], []).append(r["type"])
    for types in kinds.values():
        if "CNAME" in types and len(types) != 1:
            raise ValueError("A CNAME name must have exactly one record and no other record types.")
    h = c["dhcp"]
    start, end = (ipaddress.IPv4Address(h[k]) for k in ("pool_start", "pool_end"))
    if start not in network or end not in network or start > end or int(end) - int(start) > 65535:
        raise ValueError("The DHCP pool must be in the server subnet, in ascending order, and contain at most 65536 addresses.")
    if start == network.network_address or end == network.broadcast_address:
        raise ValueError("The DHCP pool must not include network or broadcast addresses.")
    h["pool_start"], h["pool_end"] = str(start), str(end)
    h["lease_seconds"] = int(h["lease_seconds"])
    if not 120 <= h["lease_seconds"] <= 2592000:
        raise ValueError("Lease duration must be between 120 and 2592000 seconds.")
    h["router"] = ipv4(h["router"]) if str(h["router"]).strip() else ""
    if h["router"] and (ipaddress.IPv4Address(h["router"]) not in network or
                         ipaddress.IPv4Address(h["router"]) in (network.network_address, network.broadcast_address)):
        raise ValueError("Gateway must be a host address in the server subnet.")
    h["dns_servers"] = [ipv4(x) for x in h["dns_servers"]]
    if len(h["dns_servers"]) > 8:
        raise ValueError("A maximum of eight DHCP DNS servers is supported.")
    h["domain"] = domain(h["domain"]) if str(h["domain"]).strip() else ""
    if len(h["domain"].encode()) > 255:
        raise ValueError("DHCP domain is too long.")
    used_mac, used_ip = set(), set()
    for r in h["reservations"]:
        r["mac"], r["ip"] = mac(r["mac"]), ipv4(r["ip"])
        addr = ipaddress.IPv4Address(r["ip"])
        if addr not in network or addr in (network.network_address, network.broadcast_address) or r["ip"] in (c["bind_ip"], h["router"]):
            raise ValueError("A reservation must use an available host address in the server subnet.")
        if r["mac"] in used_mac or r["ip"] in used_ip:
            raise ValueError("Duplicate DHCP reservation.")
        used_mac.add(r["mac"])
        used_ip.add(r["ip"])
    if len(h["reservations"]) > 1000 or len(h["options"]) > 50:
        raise ValueError("Too many DHCP reservations or options.")
    seen = set()
    for o in h["options"]:
        o["code"] = int(o["code"])
        if not 1 <= o["code"] <= 254 or o["code"] in {1, 3, 6, 15, 50, 51, 52, 53, 54, 55, 57, 58, 59, 61, 82}:
            raise ValueError("This DHCP option is reserved or configured using a dedicated field.")
        if o["code"] in seen:
            raise ValueError("DHCP option codes must be unique.")
        seen.add(o["code"])
        option_value(o)
    return c


def utc_timestamp(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="seconds")


# ==========================================================================
# DHCP SERVICE
# ==========================================================================

import copy
import ipaddress
import json
import socket
import struct
import sys
import threading
import time
from pathlib import Path


BOOT = struct.Struct("!BBBBIHH4s4s4s4s16s64s128s")
COOKIE = b"\x63\x82\x53\x63"
ZERO = "0.0.0.0"
NAMES = {1: "DISCOVER", 2: "OFFER", 3: "REQUEST", 4: "DECLINE", 5: "ACK", 6: "NAK", 7: "RELEASE", 8: "INFORM"}


class Packet:
    def __init__(self, data):
        if len(data) < 240 or data[236:240] != COOKIE:
            raise ValueError("Invalid DHCP packet.")
        fields = BOOT.unpack(data[:236])
        op, self.htype, self.hlen, hops, self.xid, _, self.flags = fields[:7]
        if op != 1 or self.htype != 1 or self.hlen != 6 or hops:
            raise ValueError("Only directly connected Ethernet/Wi-Fi DHCPv4 clients are supported.")
        self.ciaddr, _, _, self.giaddr = [socket.inet_ntoa(x) for x in fields[7:11]]
        self.chaddr = fields[11]
        self.mac = ":".join(f"{x:02x}" for x in self.chaddr[:6])
        self.options = {}
        index = 240
        while index < len(data):
            code = data[index]
            index += 1
            if code == 255:
                break
            if code == 0:
                continue
            if index >= len(data):
                raise ValueError("Truncated DHCP option.")
            length = data[index]
            index += 1
            if index + length > len(data):
                raise ValueError("Truncated DHCP option value.")
            self.options[code] = self.options.get(code, b"") + data[index:index + length]
            index += length
        for code, length in ((53, 1), (50, 4), (54, 4), (57, 2)):
            if code in self.options and len(self.options[code]) != length:
                raise ValueError(f"Invalid length for DHCP option {code}.")
        if 53 not in self.options:
            raise ValueError("DHCP message type is missing.")
        if 52 in self.options:
            raise ValueError("DHCP option overload is not supported.")
        self.kind = self.options[53][0]
        self.client_id = self.options.get(61)
        if self.client_id is not None and not 2 <= len(self.client_id) <= 255:
            raise ValueError("Invalid client ID.")
        self.key = "id:" + self.client_id.hex() if self.client_id else "mac:" + self.mac
        self.hostname = self.options.get(12, b"").decode("utf-8", "replace")[:128]

    def ip_option(self, code):
        return socket.inet_ntoa(self.options[code]) if code in self.options else ""


class DHCPState:
    """Serialize allocations, persist committed leases before replying with ACK."""
    def __init__(self, config, path, log):
        self.config = config
        self.h = config["dhcp"]
        self.path = Path(path)
        self.log = log
        self.lock = threading.RLock()
        self.network = ipaddress.IPv4Network(f'{config["bind_ip"]}/{config["netmask"]}', strict=False)
        self.scope = f'{config["interface"]}|{self.network}'
        self.scopes = {}
        self.leases = {}
        self.offers = {}
        self.declined = {}
        self.reservations = {r["mac"]: r["ip"] for r in self.h["reservations"]}
        self.reserved_ips = {ip: mac for mac, ip in self.reservations.items()}
        self.excluded = {config["bind_ip"], self.h["router"], *self.h["dns_servers"]}
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                self.scopes = raw["scopes"]
                if not isinstance(self.scopes, dict):
                    raise ValueError("Invalid lease file.")
                if self.scope in self.scopes:
                    current = self.scopes[self.scope]
                    self.leases = current["leases"]
                    self.declined = current.get("declined", {})
                    # Validate persisted data before it influences address assignment.
                    for value in self.leases.values():
                        ipaddress.IPv4Address(value["ip"])
                        value["expires"] = float(value["expires"])
                        if not isinstance(value["mac"], str):
                            raise ValueError("Invalid lease MAC address.")
                    for ip, expiry in self.declined.items():
                        ipaddress.IPv4Address(ip)
                        self.declined[ip] = float(expiry)
            except Exception as exc:
                raise ValueError(f"Cannot read the lease file; DHCP startup blocked to protect existing allocations: {exc}") from exc
        self.clean()
        for key, lease in self.leases.items():
            if lease["ip"] in self.excluded:
                raise ValueError(f'Active lease {lease["ip"]} conflicts with the server, gateway, or DNS address.')
            owner = self.reserved_ips.get(lease["ip"])
            if owner and owner != lease["mac"]:
                raise ValueError(f'Reservation {lease["ip"]} conflicts with an active lease. Wait for it to expire.')

    def clean(self):
        now = time.time()
        self.leases = {k: v for k, v in self.leases.items() if float(v["expires"]) > now}
        self.offers = {k: v for k, v in self.offers.items() if v["expires"] > now}
        self.declined = {k: v for k, v in self.declined.items() if float(v) > now}

    def persist(self):
        self.scopes[self.scope] = {"leases": self.leases, "declined": self.declined}
        atomic_json(self.path, {"scopes": self.scopes})

    def allowed(self, ip, hardware):
        if not ip or ip in self.excluded:
            return False
        if hardware in self.reservations:
            return ip == self.reservations[hardware]
        if ip in self.reserved_ips:
            return False
        addr = ipaddress.IPv4Address(ip)
        return ipaddress.IPv4Address(self.h["pool_start"]) <= addr <= ipaddress.IPv4Address(self.h["pool_end"])

    def free(self, ip, key):
        return (ip not in self.declined and
                all(v["ip"] != ip or k == key for k, v in self.leases.items()) and
                all(v["ip"] != ip or k == key for k, v in self.offers.items()))

    def offer(self, packet):
        with self.lock:
            self.clean()
            preferred = [self.reservations.get(packet.mac),
                         self.leases.get(packet.key, {}).get("ip"),
                         self.offers.get(packet.key, {}).get("ip"), packet.ip_option(50)]
            start = int(ipaddress.IPv4Address(self.h["pool_start"]))
            end = int(ipaddress.IPv4Address(self.h["pool_end"]))
            def candidates():
                yield from preferred
                for number in range(start, end + 1):
                    yield str(ipaddress.IPv4Address(number))
            for ip in candidates():
                if self.allowed(ip, packet.mac) and self.free(ip, packet.key):
                    self.offers[packet.key] = {"ip": ip, "mac": packet.mac, "expires": time.time() + 30}
                    return ip
            return None

    def request(self, packet):
        with self.lock:
            self.clean()
            server = packet.ip_option(54)
            if server and server != self.config["bind_ip"]:
                self.offers.pop(packet.key, None)
                return None, None
            requested = packet.ip_option(50)
            if server and (not requested or packet.ciaddr != ZERO):
                return None, None
            if requested and packet.ciaddr != ZERO:
                return None, None
            ip = requested or (packet.ciaddr if packet.ciaddr != ZERO else "")
            known = packet.key in self.leases or packet.mac in self.reservations
            # INIT-REBOOT / renewal for a client unknown to us: stay silent.
            if not server and not known:
                return None, None
            if not self.allowed(ip, packet.mac) or not self.free(ip, packet.key):
                return 6, ZERO
            old = copy.deepcopy(self.leases)
            self.leases[packet.key] = {"ip": ip, "mac": packet.mac, "hostname": packet.hostname,
                                       "expires": time.time() + self.h["lease_seconds"]}
            try:
                self.persist()
            except Exception:
                self.leases = old
                raise
            self.offers.pop(packet.key, None)
            return 5, ip

    def release(self, packet):
        with self.lock:
            self.clean()
            lease = self.leases.get(packet.key)
            if packet.ip_option(54) not in ("", self.config["bind_ip"]):
                return
            if lease and lease["ip"] == packet.ciaddr:
                # Persist first so a write failure does not free a live address in memory.
                old = self.leases.pop(packet.key)
                try:
                    self.persist()
                except Exception:
                    self.leases[packet.key] = old
                    raise
                self.offers.pop(packet.key, None)

    def decline(self, packet):
        with self.lock:
            self.clean()
            if packet.ip_option(54) != self.config["bind_ip"]:
                return
            ip = packet.ip_option(50)
            lease = self.leases.get(packet.key) or self.offers.get(packet.key)
            if lease and lease["ip"] == ip:
                old_leases, old_offers, old_declined = copy.deepcopy((self.leases, self.offers, self.declined))
                self.leases.pop(packet.key, None)
                self.offers.pop(packet.key, None)
                self.declined[ip] = time.time() + 600
                try:
                    self.persist()
                except Exception:
                    self.leases, self.offers, self.declined = old_leases, old_offers, old_declined
                    raise
                self.log.add("DHCP", f"{ip} quarantined for 10 minutes after DECLINE", "WARN")

    def snapshot(self):
        with self.lock:
            self.clean()
            result = []
            for value in self.leases.values():
                result.append({**value, "remaining": max(0, int(value["expires"] - time.time())),
                               "expires_at": utc_timestamp(value["expires"])})
            return sorted(result, key=lambda item: ipaddress.IPv4Address(item["ip"]))


class DHCPService:
    def __init__(self, config, log, lease_path):
        self.config = copy.deepcopy(config)
        self.h = self.config["dhcp"]
        self.log = log
        self.state = DHCPState(self.config, lease_path, log)
        self.sock = None
        self.thread = None
        self.stop_event = threading.Event()

    @property
    def running(self):
        return self.thread is not None and self.thread.is_alive() and not self.stop_event.is_set()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            if sys.platform == "win32":
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            bind_device(sock, self.config["interface"])
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Deliberately no SO_REUSEADDR: fail instead of sharing port 67.
            sock.bind(("", 67))
            sock.settimeout(0.5)
            self.sock = sock
            self.thread = threading.Thread(target=self.run, name="dhcp", daemon=True)
            self.thread.start()
        except Exception:
            sock.close()
            self.sock = None
            raise
        self.log.add("DHCP", f'Started on {self.config["interface"]}, UDP 67/68; '
                     f'Pool {self.h["pool_start"]}–{self.h["pool_end"]}; Gateway: {self.h["router"] or "none"}')

    def reply(self, packet, kind, ip, inform=False):
        options = [(53, bytes([kind])), (54, socket.inet_aton(self.config["bind_ip"]))]
        if packet.client_id:
            options.append((61, packet.client_id))
        if kind != 6:
            if not inform:
                seconds = self.h["lease_seconds"]
                options.extend([(51, struct.pack("!I", seconds)),
                                (58, struct.pack("!I", seconds // 2)),
                                (59, struct.pack("!I", seconds * 7 // 8))])
            options.append((1, socket.inet_aton(self.config["netmask"])))
            if self.h["router"]:
                options.append((3, socket.inet_aton(self.h["router"])))
            if self.h["dns_servers"]:
                options.append((6, b"".join(socket.inet_aton(x) for x in self.h["dns_servers"])))
            if self.h["domain"]:
                options.append((15, self.h["domain"].encode("ascii")))
            options.extend((o["code"], option_value(o)) for o in self.h["options"])
        header = BOOT.pack(2, packet.htype, packet.hlen, 0, packet.xid, 0, packet.flags,
                           socket.inet_aton(packet.ciaddr if kind != 6 else ZERO), socket.inet_aton(ip),
                           b"\0" * 4, b"\0" * 4, packet.chaddr, b"\0" * 64, b"\0" * 128)
        size = struct.unpack("!H", packet.options.get(57, struct.pack("!H", 576)))[0]
        limit = min(1472, max(576, size))
        data = bytearray(header + COOKIE)
        for code, value in options:
            if len(data) + 3 + len(value) > limit:
                self.log.add("DHCP", f"Option {code} exceeds client packet size {limit}; omitted", "WARN")
                continue
            data.extend(bytes([code, len(value)]) + value)
        data.append(255)
        data.extend(b"\0" * max(0, 300 - len(data)))
        # No configured IP at bootstrap: broadcast also avoids an unresolvable ARP lookup.
        target = "255.255.255.255" if kind == 6 or packet.ciaddr == ZERO or packet.flags & 0x8000 else packet.ciaddr
        return bytes(data), (target, 68)

    def handle(self, data, peer):
        if peer[1] != 68:
            return None
        packet = Packet(data)
        if packet.giaddr != ZERO:
            self.log.add("DHCP", "DHCP relay packet ignored (direct subnet only)", "WARN")
            return None
        if peer[0] != ZERO and ipaddress.IPv4Address(peer[0]) not in self.state.network:
            return None
        self.log.add("DHCP", f'{NAMES.get(packet.kind, packet.kind)} from {packet.mac} '
                     f'({packet.hostname or "no hostname"}), xid={packet.xid:08x}')
        kind, ip = None, None
        if packet.kind == 1:
            if packet.ciaddr != ZERO:
                return None
            ip = self.state.offer(packet)
            if ip:
                kind = 2
            else:
                self.log.add("DHCP", f"No available address for {packet.mac}", "WARN")
        elif packet.kind == 3:
            kind, ip = self.state.request(packet)
        elif packet.kind == 4:
            self.state.decline(packet)
        elif packet.kind == 7:
            self.state.release(packet)
        elif packet.kind == 8 and packet.ciaddr != ZERO:
            if ipaddress.IPv4Address(packet.ciaddr) in self.state.network:
                kind, ip = 5, ZERO
        if kind:
            self.log.add("DHCP", f'{NAMES[kind]} → {packet.mac}, IP {ip}')
            return self.reply(packet, kind, ip, inform=packet.kind == 8)
        return None

    def run(self):
        try:
            while not self.stop_event.is_set():
                try:
                    data, peer = self.sock.recvfrom(4096)
                    answer = self.handle(data, peer)
                    if answer:
                        self.sock.sendto(*answer)
                except socket.timeout:
                    continue
                except OSError as exc:
                    if not self.stop_event.is_set():
                        self.log.add("DHCP", f"Socket or storage error: {exc}", "ERROR")
                        # A closed/invalid socket must not spin indefinitely.
                        if exc.errno in (9, 38, 88, 10038):
                            break
                except Exception as exc:
                    self.log.add("DHCP", f"Packet dropped: {exc}", "WARN")
        finally:
            self.stop_event.set()
            if self.sock:
                self.sock.close()

    def stop(self):
        self.stop_event.set()
        if self.sock:
            self.sock.close()
        if self.thread:
            self.thread.join(timeout=2)
        self.sock = None
        self.thread = None


# ==========================================================================
# DNS SERVICE
# ==========================================================================

import copy
import secrets
import socket
import socketserver
import struct
import threading




def receive_exact(sock, length):
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("DNS TCP connection ended prematurely.")
        data.extend(chunk)
    return bytes(data)


class BoundedThreads(socketserver.ThreadingMixIn):
    daemon_threads = True
    block_on_close = False

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def handle_error(self, request, client_address):
        self.service.log.add("DNS", f"Error handling query from {client_address[0]}", "ERROR")


class UDPServer(BoundedThreads, socketserver.UDPServer):
    allow_reuse_address = False


class TCPServer(BoundedThreads, socketserver.TCPServer):
    allow_reuse_address = True


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        service = self.server.service
        if self.server.socket_type == socket.SOCK_DGRAM:
            data, sock = self.request
            response = service.answer(data, self.client_address[0], tcp=False)
            if response:
                sock.sendto(response, self.client_address)
        else:
            self.request.settimeout(3)
            try:
                for _ in range(32):
                    size = struct.unpack("!H", receive_exact(self.request, 2))[0]
                    if not size:
                        return
                    response = service.answer(receive_exact(self.request, size), self.client_address[0], tcp=True)
                    if not response:
                        return
                    self.request.sendall(struct.pack("!H", len(response)) + response)
            except (OSError, ConnectionError):
                return


class DNSService:
    def __init__(self, config, log):
        self.config = copy.deepcopy(config)
        self.settings = self.config["dns"]
        self.log = log
        self.servers = []
        self.threads = []

    @property
    def running(self):
        return bool(self.threads) and all(t.is_alive() for t in self.threads)

    def start(self):
        try:
            for cls in (UDPServer, TCPServer):
                server = cls((self.config["bind_ip"], self.settings["port"]), Handler)
                server.service = self
                server.slots = threading.BoundedSemaphore(64)
                self.servers.append(server)
            for server in self.servers:
                thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
                thread.start()
                self.threads.append(thread)
        except Exception:
            self.stop()
            raise
        self.log.add("DNS", f'Started: {self.config["bind_ip"]}:{self.settings["port"]}, UDP + TCP')

    def stop(self):
        for i, server in enumerate(self.servers):
            if i < len(self.threads) and self.threads[i].is_alive():
                server.shutdown()
            server.server_close()
        self.servers.clear()
        for t in self.threads:
            t.join(timeout=1)
        self.threads.clear()

    def forward(self, request):
        if not request.header.rd:
            response = request.reply(aa=0, ra=bool(self.settings["forwarders"]))
            response.header.rcode = RCODE.REFUSED
            return response
        last_error = "No forwarder configured"
        for address in self.settings["forwarders"]:
            host, port = endpoint(address)
            upstream = DNSRecord.parse(request.pack())
            upstream.header.id = secrets.randbits(16)
            family = socket.AF_INET6 if ":" in host else socket.AF_INET
            try:
                with socket.socket(family, socket.SOCK_DGRAM) as sock:
                    sock.settimeout(self.settings["timeout"])
                    sock.connect((host, port))
                    sock.send(upstream.pack())
                    data = sock.recv(65535)
                response = DNSRecord.parse(data)
                self.check_upstream(upstream, response)
                if response.header.tc:
                    with socket.socket(family, socket.SOCK_STREAM) as sock:
                        sock.settimeout(self.settings["timeout"])
                        sock.connect((host, port))
                        data = upstream.pack()
                        sock.sendall(struct.pack("!H", len(data)) + data)
                        size = struct.unpack("!H", receive_exact(sock, 2))[0]
                        response = DNSRecord.parse(receive_exact(sock, size))
                        self.check_upstream(upstream, response)
                if response.header.rcode in (RCODE.SERVFAIL, RCODE.REFUSED):
                    raise ValueError(RCODE[response.header.rcode])
                response.header.id = request.header.id
                return response
            except Exception as exc:
                last_error = f"{address}: {exc}"
                self.log.add("DNS", f"Forwarder failed: {last_error}", "WARN")
        response = request.reply(aa=0, ra=bool(self.settings["forwarders"]))
        response.header.rcode = RCODE.SERVFAIL if self.settings["forwarders"] else RCODE.REFUSED
        return response

    @staticmethod
    def check_upstream(request, response):
        if (not response.header.qr or response.header.id != request.header.id or
                response.header.opcode != request.header.opcode or len(response.questions) != 1 or
                response.q != request.q):
            raise ValueError("Forwarder response does not match the query.")

    def records_for(self, name):
        records = self.settings["records"]
        exact = [r for r in records if r["name"] == name]
        if exact:
            return exact
        labels = name.split(".")
        for i in range(1, len(labels)):
            wildcard = "*." + ".".join(labels[i:])
            found = [r for r in records if r["name"] == wildcard]
            if found:
                return found
        return []

    def resolve(self, request, depth=0):
        reply = request.reply(aa=1, ra=bool(self.settings["forwarders"]))
        if depth >= 8:
            reply.header.rcode = RCODE.SERVFAIL
            return reply
        name = str(request.q.qname).rstrip(".").lower()
        records = self.records_for(name)
        if records:
            for record in records:
                if request.q.qtype in (QTYPE.ANY, getattr(QTYPE, record["type"])) or record["type"] == "CNAME":
                    reply.add_answer(RR(request.q.qname, getattr(QTYPE, record["type"]),
                                        ttl=record["ttl"], rdata=rdata(record)))
                    if record["type"] == "CNAME" and request.q.qtype in (QTYPE.A, QTYPE.AAAA, QTYPE.MX, QTYPE.PTR, QTYPE.TXT):
                        follow = DNSRecord.question(str(rdata(record)), QTYPE[request.q.qtype])
                        follow.header.rd = request.header.rd
                        target = self.resolve(follow, depth + 1)
                        reply.header.rcode = target.header.rcode
                        reply.add_answer(*target.rr)
            return reply
        zone = self.settings["local_zone"]
        # Local names, including empty non-terminals, never leak to a forwarder.
        child_exists = any(r["name"].endswith("." + name) for r in self.settings["records"])
        if child_exists or (zone and (name == zone or name.endswith("." + zone))):
            reply.header.rcode = RCODE.NOERROR if child_exists or name == zone else RCODE.NXDOMAIN
            return reply
        if request.q.qtype == QTYPE.ANY:
            reply.header.aa = 0
            reply.header.rcode = RCODE.REFUSED
            return reply
        return self.forward(request)

    def answer(self, data, client, tcp=False):
        try:
            request = DNSRecord.parse(data)
            if request.header.qr:
                return None
            reply = request.reply(aa=0, ra=bool(self.settings["forwarders"]))
            if len(request.questions) != 1:
                reply.header.rcode = RCODE.FORMERR
            elif request.header.opcode != 0:
                reply.header.rcode = RCODE.NOTIMP
            elif request.q.qclass != 1:
                reply.header.rcode = RCODE.REFUSED
            else:
                reply = self.resolve(request)
            packed = reply.pack()
            if not tcp:
                size = next((r.rclass for r in request.ar if r.rtype == QTYPE.OPT), 512)
                limit = min(1232, max(512, size))
                if len(packed) > limit:
                    reply = request.reply(aa=reply.header.aa, ra=reply.header.ra)
                    reply.header.tc = 1
                    packed = reply.pack()
            q = str(request.q) if request.questions else "<no question>"
            self.log.add("DNS", f'{client} {"TCP" if tcp else "UDP"} {q} → {RCODE[reply.header.rcode]}, {len(reply.rr)} answers')
            return packed
        except Exception as exc:
            self.log.add("DNS", f"Invalid query from {client}: {exc}", "WARN")
            return None


# ==========================================================================
# APP
# ==========================================================================

import argparse
import copy
import errno
import json
import secrets
import signal
import socket
import struct
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parent
DEFAULT_UI_PORTS = (8080, 8090, 18080, 0)


class Application:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.path = self.data_dir / "config.json"
        self.log = EventLog()
        self.lock = threading.RLock()
        self.token = secrets.token_urlsafe(32)
        self.dns = None
        self.dhcp = None
        self.config = copy.deepcopy(DEFAULTS)
        if self.path.exists():
            self.config = validate(json.loads(self.path.read_text(encoding="utf-8")))
        self.log.add("SYSTEM", "Console ready. DNS and DHCP are stopped.")

    def state(self):
        with self.lock:
            return {"dns_running": bool(self.dns and self.dns.running),
                    "dhcp_running": bool(self.dhcp and self.dhcp.running),
                    "dhcp_supported": sys.platform in ("win32", "darwin") or sys.platform.startswith("linux"),
                    "platform": sys.platform, "interfaces": interfaces(),
                    "leases": self.dhcp.state.snapshot() if self.dhcp else []}

    def action(self, action, payload):
        with self.lock:
            if action == "save":
                if (self.dns and self.dns.running) or (self.dhcp and self.dhcp.running):
                    raise ValueError("Stop both services before saving, then restart the services you need.")
                updated = validate(payload)
                atomic_json(self.path, updated)
                self.config = updated
                self.log.add("SYSTEM", "Configuration saved.")
                return {"ok": True, "config": self.config}
            if action not in ("start_dns", "stop_dns", "start_dhcp", "stop_dhcp"):
                raise ValueError("Unknown action.")
            name = action.split("_", 1)[1]
            service = getattr(self, name)
            if action.startswith("stop_"):
                if service:
                    service.stop()
                self.log.add(name.upper(), "Service stopped.")
            elif service and service.running:
                return {"ok": True}
            else:
                config = validate(self.config)
                check_interface(config)
                if service:
                    service.stop()
                if name == "dns":
                    new_service = DNSService(config, self.log)
                else:
                    if not self.state()["dhcp_supported"]:
                        raise ValueError("DHCP requires Windows, macOS, or Linux.")
                    if config["bind_ip"] in config["dhcp"]["dns_servers"]:
                        if config["dns"]["port"] != 53:
                            raise ValueError("The local DNS server must use port 53 when its address is advertised by DHCP.")
                        if not self.dns or not self.dns.running:
                            self.log.add("DHCP", "DHCP advertises the local DNS server, but DNS is stopped.", "WARN")
                    new_service = DHCPService(config, self.log, self.data_dir / "leases.json")
                try:
                    new_service.start()
                except PermissionError as exc:
                    new_service.stop()
                    raise ValueError("Permission denied opening the service port or binding the interface. "
                                     "Windows: open a terminal as administrator; "
                                     "macOS/Linux: run sudo python3 lantern.py.") from exc
                except OSError as exc:
                    new_service.stop()
                    raise ValueError(f"Service could not start: {exc}. Check the IP address; the port may already be in use.") from exc
                except Exception:
                    new_service.stop()
                    raise
                setattr(self, name, new_service)
            return {"ok": True}

    def close(self):
        with self.lock:
            if self.dhcp:
                self.dhcp.stop()
            if self.dns:
                self.dns.stop()


class AdminServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = sys.platform != "win32"

    def server_bind(self):
        if sys.platform == "win32":
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()

    def get_request(self):
        request, address = super().get_request()
        request.settimeout(10)
        return request, address


class AdminHandler(BaseHTTPRequestHandler):
    server_version = "LANtern/2.0"

    def log_message(self, *args):
        pass

    def send(self, status, value, content_type="application/json; charset=utf-8"):
        data = json.dumps(value, ensure_ascii=False).encode() if content_type.startswith("application/json") else value
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                         "style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    def permitted(self, api=False):
        port = self.server.server_port
        if self.headers.get("Host") not in (f"127.0.0.1:{port}", f"localhost:{port}"):
            self.send(403, {"error": "Invalid host. Open the console using 127.0.0.1."})
            return False
        origin = self.headers.get("Origin")
        if origin and origin not in (f"http://127.0.0.1:{port}", f"http://localhost:{port}"):
            self.send(403, {"error": "Cross-origin requests are not allowed."})
            return False
        if api and not secrets.compare_digest(self.headers.get("X-Admin-Token", ""), self.server.app.token):
            self.send(403, {"error": "Invalid session. Reload the page."})
            return False
        return True

    def do_GET(self):
        parsed = urlsplit(self.path)
        if not self.permitted(api=parsed.path.startswith("/api/")):
            return
        app = self.server.app
        try:
            if parsed.path == "/":
                html = HTML.replace("__ADMIN_TOKEN__", app.token)
                self.send(200, html.encode(), "text/html; charset=utf-8")
            elif parsed.path == "/api/state":
                self.send(200, app.state())
            elif parsed.path == "/api/config":
                with app.lock:
                    self.send(200, app.config)
            elif parsed.path == "/api/logs":
                cursor = int(parse_qs(parsed.query).get("after", ["0"])[0])
                self.send(200, app.log.since(cursor))
            else:
                self.send(404, {"error": "Not found."})
        except (ValueError, TypeError) as exc:
            self.send(400, {"error": str(exc)})
        except Exception as exc:
            app.log.add("SYSTEM", str(exc), "ERROR")
            self.send(500, {"error": "Internal error. Check the activity log."})

    def do_POST(self):
        if not self.permitted(api=True):
            return
        app = self.server.app
        try:
            if self.path != "/api/action":
                self.send(404, {"error": "Not found."})
                return
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 262144:
                raise ValueError("Request must contain 1–262144 bytes.")
            if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                raise ValueError("Expected JSON.")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("Expected a JSON object.")
            result = app.action(str(body.get("action", "")), body.get("config"))
            self.send(200, result)
        except (ValueError, TypeError, KeyError, AttributeError, OverflowError, struct.error) as exc:
            message = f"Invalid or incomplete setting: {exc}"
            app.log.add("SYSTEM", message, "WARN")
            self.send(400, {"error": message})
        except Exception as exc:
            app.log.add("SYSTEM", str(exc), "ERROR")
            self.send(500, {"error": f"Error: {exc}"})


def open_admin_server(port=None):
    """Choose an available loopback port unless an exact port was requested."""
    for candidate in ((port,) if port is not None else DEFAULT_UI_PORTS):
        try:
            return AdminServer(("127.0.0.1", candidate), AdminHandler)
        except OSError as exc:
            if port is not None or exc.errno not in (errno.EACCES, errno.EADDRINUSE, 10013, 10048):
                raise
    raise OSError("No local port is available for the console.")


def main():
    parser = argparse.ArgumentParser(description="Local DNS/DHCP server with a browser console")
    parser.add_argument("--ui-port", type=int, default=None,
                        help="Fixed port; default is 8080 with automatic fallback")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()
    if args.ui_port is not None and not 1 <= args.ui_port <= 65535:
        parser.error("Console port must be between 1 and 65535.")
    if args.data_dir.is_symlink():
        parser.error("The data directory must not be a symbolic link.")
    try:
        app = Application(args.data_dir)
        server = open_admin_server(args.ui_port)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"Startup failed: {exc}\nFor port errors, choose a different port: "
                         "python3 lantern.py --ui-port 8090") from exc
    server.app = app
    url = f"http://127.0.0.1:{server.server_port}"
    if args.ui_port is None and server.server_port != 8080:
        print(f"Port 8080 is unavailable. Using port {server.server_port}.", flush=True)
    print(f"\nLANtern\nConsole: {url}\nDNS and DHCP are initially stopped.\nQuit: Ctrl+C\n", flush=True)
    if args.open_browser:
        webbrowser.open(url)

    def shutdown(*_):
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        app.close()
        server.server_close()


if __name__ == "__main__":
    main()
