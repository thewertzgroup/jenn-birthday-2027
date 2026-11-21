(function(){
  var el=document.getElementById('leaflet'); if(!el||!window.L) return;
  var P={dub:[53.3438,-6.2546,'Dublin'],kil:[52.6503,-7.2490,'Kilkenny'],kry:[52.0599,-9.5044,'Killarney'],
    adr:[52.5640,-8.7901,'★ Adare Manor'],ash:[53.5420,-9.2850,'Ashford Castle'],noc:[53.9103,-8.8185,'Knock'],
    snn:[52.7020,-8.9248,'Shannon'],lon:[51.5045,-0.1500,'London'],lgw:[51.1537,-0.1821,'Gatwick'],
    nce:[43.6970,7.2700,'Nice'],mco:[43.7384,7.4246,'Monaco'],par:[48.8670,2.3270,'Paris'],ncea:[43.6970,7.2700,'★ Nice (birthday)']};
  var map=L.map(el,{scrollWheelZoom:false,tap:true});
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap contributors'}).addTo(map);
  var routes={
    B:{drive:[['dub','kil'],['kil','kry'],['kry','adr'],['adr','ash'],['ash','noc'],['lon','lgw']],fly:[['noc','lon'],['lgw','nce'],['nce','par']],stops:['dub','kil','kry','adr','ash','noc','lon','nce','mco','par']},
    A:{drive:[['ncea','mco']],fly:[['dub','ncea'],['mco','par']],stops:['dub','ncea','mco','par']}
  };
  var layer=null;
  function ll(k){return [P[k][0],P[k][1]];}
  function show(v){
    if(layer) map.removeLayer(layer);
    layer=L.layerGroup().addTo(map); var r=routes[v], pts=[];
    r.drive.forEach(function(s){L.polyline([ll(s[0]),ll(s[1])],{color:'#38bdf8',weight:4,opacity:.9}).addTo(layer);});
    r.fly.forEach(function(s){L.polyline([ll(s[0]),ll(s[1])],{color:'#a78bfa',weight:3,dashArray:'7 7',opacity:.95}).addTo(layer);});
    r.stops.forEach(function(k){var star=P[k][2].indexOf('★')===0;pts.push(ll(k));
      L.circleMarker(ll(k),{radius:star?9:6,color:'#fff',weight:2,fillColor:star?'#fbbf24':'#38bdf8',fillOpacity:1}).addTo(layer)
       .bindTooltip(P[k][2],{permanent:true,direction:'right',offset:[8,0],className:'lbl'});});
    map.fitBounds(pts,{padding:[24,24]});
  }
  show('B');
  document.querySelectorAll('.map-toggle button').forEach(function(b){b.addEventListener('click',function(){
    document.querySelectorAll('.map-toggle button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
    show(b.dataset.route);});});
})();
