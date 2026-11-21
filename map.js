(function(){
  var el=document.getElementById('leaflet'); if(!el||!window.L) return;
  var P={dub:[53.3382,-6.2591,'Dublin'],kry:[52.0599,-9.5044,'Killarney'],moh:[52.9715,-9.4309,'Cliffs of Moher'],
    ash:[53.5420,-9.2850,'★ Ashford Castle'],noc:[53.9103,-8.8185,'Knock'],lon:[51.5076,-0.1527,'London'],
    nce:[43.6950,7.2650,'Nice'],mco:[43.7384,7.4246,'Monaco']};
  var map=L.map(el,{scrollWheelZoom:false,zoomSnap:0.25});
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap contributors'}).addTo(map);
  function ll(k){return [P[k][0],P[k][1]];}
  [['dub','kry'],['kry','moh'],['moh','ash'],['ash','noc']].forEach(function(s){L.polyline([ll(s[0]),ll(s[1])],{color:'#38bdf8',weight:4,opacity:.9}).addTo(map);});
  L.polyline([ll('nce'),ll('mco')],{color:'#38bdf8',weight:3,opacity:.7,dashArray:'2 6'}).addTo(map);
  [['noc','lon'],['lon','nce']].forEach(function(s){L.polyline([ll(s[0]),ll(s[1])],{color:'#a78bfa',weight:3,dashArray:'7 7',opacity:.95}).addTo(map);});
  var MAJOR=['dub','ash','lon','nce','mco'], DIR={kry:'left',moh:'left',ash:'top',noc:'right',dub:'right',lon:'right',nce:'left',mco:'top'};
  var pts=[];
  Object.keys(P).forEach(function(k){var star=k==='ash';pts.push(ll(k));
    var d=DIR[k]||'right';
    L.circleMarker(ll(k),{radius:star?9:6,color:'#fff',weight:2,fillColor:star?'#fbbf24':'#38bdf8',fillOpacity:1}).addTo(map)
     .bindTooltip(P[k][2],{permanent:true,direction:d,offset:d==='top'?[0,-8]:(d==='left'?[-8,0]:[8,0]),className:MAJOR.indexOf(k)>=0?'lbl':'lbl minor'});});
  function all(){map.fitBounds(pts,{paddingTopLeft:[30,30],paddingBottomRight:[60,20]});}
  function ie(){map.fitBounds([[51.8,-10.3],[54.1,-6.0]],{padding:[10,10]});}
  function zc(){el.classList.toggle('far',map.getZoom()<6);}
  map.on('zoomend',zc); all(); zc();
  var bA=document.getElementById('zoom-all'), bI=document.getElementById('zoom-ie');
  function press(b){[bA,bI].forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});}
  bA.addEventListener('click',function(){press(bA);all();}); bI.addEventListener('click',function(){press(bI);ie();});
})();
