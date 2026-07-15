/* Who Owns Nashville - reusable boundary/reference layer catalog.
   Usage on any Leaflet page:
     <script src="won_boundary_layers.js"></script>
     var ctl = L.control.layers(BASES, null, {...}).addTo(map);
     WON_LAYERS.attach(map, ctl);   // adds every layer as a lazy overlay toggle
   Layers fetch from the source ArcGIS service only when first switched on,
   paging past the per-request record cap. Nothing loads until toggled.
   Full source list with notes: _BOUNDARY_LAYERS_REFERENCE.md */
var WON_LAYERS = (function () {
  var CATALOG = [
    { key: 'county', label: 'County boundary', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Davidson_County_Boundary_1/FeatureServer/0',
      style: { color: '#1a3a5c', weight: 2, fillOpacity: 0, dashArray: '4,4' } },
    { key: 'county_buffer', label: 'County buffer', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/DavidsonCountyBoundaryBuffer/FeatureServer/0',
      style: { color: '#9aa0a6', weight: 1, fillColor: '#e9edf1', fillOpacity: 0.55 } },
    { key: 'zips', label: 'ZIP codes', kind: 'geojson',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Boundaries/Boundaries/MapServer/0',
      style: { color: '#8a6100', weight: 1.2, fillOpacity: 0.03 },
      nameFields: ['ZIP', 'ZIPCODE', 'ZIP_CODE', 'NAME'] },
    { key: 'planning', label: 'Community planning areas', kind: 'geojson',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Boundaries/Boundaries/MapServer/1',
      style: { color: '#1e7a48', weight: 1.4, fillOpacity: 0.03 },
      nameFields: ['NAME', 'PLAN_AREA', 'AREA_NAME', 'COMMUNITY'] },
    { key: 'council', label: 'Council districts (2022, demographics)', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/2022_CouncilDistricts_with_Demographics/FeatureServer/0',
      style: { color: '#6b3fa0', weight: 1.4, fillOpacity: 0.03 },
      nameFields: ['DISTRICT', 'CouncilDistrict', 'COUNCILDIS', 'NAME'] },
    { key: 'council_prof', label: 'Council district profiles', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Council_District_Demographic_Profiles_Public_view/FeatureServer/0',
      style: { color: '#6b3fa0', weight: 1, dashArray: '2,3', fillOpacity: 0.02 },
      nameFields: ['DISTRICT', 'NAME'] },
    { key: 'tracts', label: 'Census tracts', kind: 'geojson',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/2',
      style: { color: '#1c458c', weight: 1, fillOpacity: 0.02 },
      nameFields: ['TRACTCE', 'TRACT', 'NAME', 'GEOID'] },
    { key: 'blockgroups', label: 'Census block groups', kind: 'geojson',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/1',
      style: { color: '#1c458c', weight: 0.8, dashArray: '2,3', fillOpacity: 0.02 },
      nameFields: ['GEOID', 'NAME', 'BLKGRPCE'] },
    { key: 'blocks', label: 'Census blocks (heavy)', kind: 'geojson',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/0',
      style: { color: '#66707c', weight: 0.5, fillOpacity: 0.01 },
      nameFields: ['GEOID', 'NAME', 'BLOCKCE'] },
    { key: 'subdivisions', label: 'Subdivisions (heavy)', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Subdivision_Boundaries/FeatureServer/0',
      style: { color: '#c0392b', weight: 0.7, fillOpacity: 0.02 },
      nameFields: ['SUBDIVISIO', 'SUBDIVISION', 'NAME', 'SubName'] },
    { key: 'communities', label: 'Community name points', kind: 'geojson',
      url: 'https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Davidson_County_Communities_view/FeatureServer/0',
      point: true, nameFields: ['NAME', 'COMMUNITY', 'Community_Name', 'LABEL'] },
    { key: 'tn_counties', label: 'TN county boundaries', kind: 'geojson',
      url: 'https://services1.arcgis.com/kILp9lqGUeOhnDbI/ArcGIS/rest/services/TN_County_Layer/FeatureServer/0',
      style: { color: '#5b6675', weight: 1, fillOpacity: 0 },
      nameFields: ['NAME', 'COUNTY', 'CNTY_NAME'] },
    { key: 'tn_state', label: 'TN state boundary', kind: 'geojson',
      url: 'https://services4.arcgis.com/QdHwhlbx61LR3TWb/ArcGIS/rest/services/TN_Boundary/FeatureServer/0',
      style: { color: '#20303f', weight: 2, fillOpacity: 0 } },
    /* tile basemap: Metro's muted Nashville basemap (cached MapServer) */
    { key: 'muted_base', label: 'Nashville Muted (Metro)', kind: 'tiles',
      url: 'https://maps.nashville.gov/arcgis/rest/services/Basemaps/NashvilleBasemapMuted/MapServer' }
    /* reference-only services (query on demand, not toggle layers):
       - Cadastral parcels (live):  https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer  (layer 4 = current parcels)
       - TN statewide IMPACT dir:   https://maps.cot.tn.gov/server3/rest/services/IMPACT */
  ];

  var PAGE = 2000, MAXPAGES = 40;
  function fetchPage(url, offset) {
    return fetch(url + '/query?where=1%3D1&outFields=*&outSR=4326&f=geojson&resultRecordCount=' + PAGE + '&resultOffset=' + offset)
      .then(function (r) { return r.json(); });
  }
  var cache = {};
  function load(key) {
    var e = CATALOG.filter(function (x) { return x.key === key; })[0];
    if (!e || e.kind !== 'geojson') return Promise.reject('unknown layer ' + key);
    if (cache[key]) return cache[key];
    cache[key] = new Promise(function (resolve, reject) {
      var feats = [];
      function step(page) {
        fetchPage(e.url, page * PAGE).then(function (gj) {
          var f = (gj && gj.features) || [];
          feats = feats.concat(f);
          if (f.length === PAGE && page + 1 < MAXPAGES) step(page + 1);
          else resolve({ type: 'FeatureCollection', features: feats });
        }).catch(reject);
      }
      step(0);
    });
    return cache[key];
  }
  function nameOf(props, fields) {
    if (!props) return '';
    for (var i = 0; i < (fields || []).length; i++) {
      var want = fields[i].toLowerCase();
      for (var k in props) if (k.toLowerCase() === want && props[k] != null && props[k] !== '') return String(props[k]);
    }
    return '';
  }
  function attach(map, ctl, opts) {
    opts = opts || {};
    CATALOG.forEach(function (e) {
      if (e.kind === 'tiles') {
        if (opts.tiles !== false) ctl.addBaseLayer(L.tileLayer(e.url + '/tile/{z}/{y}/{x}', { attribution: 'Metro Nashville', maxZoom: 19 }), e.label);
        return;
      }
      if (e.kind !== 'geojson') return;
      e._group = L.layerGroup();
      ctl.addOverlay(e._group, e.label);
    });
    map.on('overlayadd', function (ev) {
      var e = CATALOG.filter(function (x) { return x._group === ev.layer; })[0];
      if (!e || e._loaded) return;
      e._loaded = 1;
      load(e.key).then(function (gj) {
        L.geoJSON(gj, {
          style: e.style,
          pointToLayer: function (f, ll) {
            return L.circleMarker(ll, { radius: 3, color: '#20303f', weight: 1, fillColor: '#f0af1e', fillOpacity: 0.9 });
          },
          onEachFeature: function (f, lyr) {
            var nm = nameOf(f.properties, e.nameFields);
            if (nm) lyr.bindTooltip(nm, { sticky: true });
          }
        }).addTo(e._group);
      }).catch(function () {
        e._loaded = 0; /* allow retry on next toggle */
        console.warn('WON_LAYERS: could not load', e.key);
      });
    });
  }
  return { CATALOG: CATALOG, load: load, attach: attach };
})();
