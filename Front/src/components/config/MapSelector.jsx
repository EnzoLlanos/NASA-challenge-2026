import { useEffect, useRef } from "react";

const DEMO = { lat: -33.675, lng: -65.457 };

export default function MapSelector({ selectedLocation, onLocationChange, onLoadDemo }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);
  const markerRef = useRef(null);
  const polygonRef = useRef(null);
  const onChangeRef = useRef(onLocationChange);
  onChangeRef.current = onLocationChange;

  // Inicializa el mapa una sola vez
  useEffect(() => {
    const L = window.L;
    if (!L || !containerRef.current) return;

    const start = selectedLocation || DEMO;
    const map = L.map(containerRef.current, { center: [start.lat, start.lng], zoom: 12 });

    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      { maxZoom: 18 }
    ).addTo(map);

    const marker = L.marker([start.lat, start.lng], { draggable: true }).addTo(map);
    marker.on("dragend", (e) => {
      const p = e.target.getLatLng();
      onChangeRef.current({ lat: +p.lat.toFixed(5), lng: +p.lng.toFixed(5) });
    });
    map.on("click", (e) => {
      onChangeRef.current({ lat: +e.latlng.lat.toFixed(5), lng: +e.latlng.lng.toFixed(5) });
    });

    mapRef.current = map;
    markerRef.current = marker;
    setTimeout(() => map.invalidateSize(), 100);

    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sincroniza marcador con la ubicación elegida
  useEffect(() => {
    const L = window.L;
    const map = mapRef.current;
    if (!L || !map || !selectedLocation) return;
    const { lat, lng } = selectedLocation;

    markerRef.current.setLatLng([lat, lng]);
    map.flyTo([lat, lng], Math.max(map.getZoom(), 13), { duration: 1 });

    if (polygonRef.current) {
      map.removeLayer(polygonRef.current);
      polygonRef.current = null;
    }
    if (Math.abs(lat - DEMO.lat) < 0.0001 && Math.abs(lng - DEMO.lng) < 0.0001) {
      polygonRef.current = L.polygon(
        [
          [lat - 0.006, lng - 0.008],
          [lat + 0.006, lng - 0.008],
          [lat + 0.006, lng + 0.008],
          [lat - 0.006, lng + 0.008]
        ],
        { color: "#22c55e", fillColor: "#4ade80", fillOpacity: 0.35, weight: 2 }
      ).addTo(map);
    }
  }, [selectedLocation]);

  return (
    <div className="map-card">
      <div className="map-card-header">
        <h2>📍 Tu campo en el mapa</h2>
        <button type="button" className="btn-demo-sanluis" onClick={onLoadDemo}>
          🎯 Cargar lote de ejemplo - San Luis
        </button>
      </div>

      <div className="leaflet-map-wrapper" ref={containerRef}>
        {!window.L && <p style={{ padding: 12 }}>No se pudo cargar el mapa (revisá tu conexión a internet).</p>}
      </div>

      <div className="coords-indicator">
        <span><strong>Lat:</strong> {selectedLocation?.lat}</span>
        <span><strong>Lng:</strong> {selectedLocation?.lng}</span>
        <span>Hacé clic en el mapa para marcar tu lote</span>
      </div>
    </div>
  );
}
