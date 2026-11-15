import { useEffect, useRef } from "react";
import {
  SAN_LUIS_PROVINCE_BORDER,
  SAN_LUIS_ZONES,
  SAN_LUIS_DEPARTMENTS
} from "../../data/sanLuisGeo";

export default function MapSelector({ isOpen, selectedRegion, onSelectRegion, onClose }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;
    const L = window.L;
    if (!L || !containerRef.current) return;

    const map = L.map(containerRef.current, {
      center: [-33.75, -66.02],
      zoom: 7.4,
      zoomSnap: 0.25,
      zoomDelta: 0.5,
      minZoom: 6.5,
      maxZoom: 13,
      zoomControl: true
    });

    // Mapa base satelital (Esri World Imagery)
    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        maxZoom: 18,
        attribution: "Tiles &copy; Esri"
      }
    ).addTo(map);

    // Capa de ciudades, rutas y nombres de lugares (solo se activa al hacer zoom >= 8)
    const placesOverlay = L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
      {
        maxZoom: 18,
        pane: "overlayPane"
      }
    );

    const deptMarkers = [];

    const syncZoomVisibility = () => {
      const currentZoom = map.getZoom();
      if (currentZoom >= 8) {
        if (!map.hasLayer(placesOverlay)) {
          placesOverlay.addTo(map);
        }
        deptMarkers.forEach((m) => {
          if (!map.hasLayer(m)) m.addTo(map);
        });
      } else {
        if (map.hasLayer(placesOverlay)) {
          map.removeLayer(placesOverlay);
        }
        deptMarkers.forEach((m) => {
          if (map.hasLayer(m)) map.removeLayer(m);
        });
      }
    };

    map.on("zoomend", syncZoomVisibility);

    // Máscara oscura exterior para resaltar únicamente la provincia de San Luis
    const worldRing = [
      [-90, -180],
      [90, -180],
      [90, 180],
      [-90, 180]
    ];
    L.polygon([worldRing, SAN_LUIS_PROVINCE_BORDER], {
      stroke: false,
      fillColor: "#040b06",
      fillOpacity: 0.65,
      interactive: false
    }).addTo(map);

    // 1. Límites de los 9 departamentos de San Luis (siempre visibles; sus nombres solo al hacer zoom)
    SAN_LUIS_DEPARTMENTS.forEach((dept) => {
      L.polygon(dept.coords, {
        color: "rgba(255, 255, 255, 0.55)",
        weight: 1.2,
        dashArray: "4, 4",
        fill: false,
        interactive: false
      }).addTo(map);

      const deptLabel = L.divIcon({
        className: "dept-map-label",
        html: `<span>${dept.name}</span>`,
        iconSize: [110, 18],
        iconAnchor: [55, 9]
      });
      const marker = L.marker(dept.labelPos, { icon: deptLabel, interactive: false });
      deptMarkers.push(marker);
    });

    // 2. Las 3 zonas seleccionables (NORTE, CENTRO, SUR) recortadas con el borde real de San Luis
    SAN_LUIS_ZONES.forEach((zone) => {
      const isSelected = selectedRegion === zone.id;

      const poly = L.polygon(zone.coords, {
        color: "#ffffff",
        weight: isSelected ? 3.5 : 2,
        fillColor: zone.color,
        fillOpacity: isSelected ? 0.42 : 0.18
      }).addTo(map);

      const zoneBadge = L.divIcon({
        className: "zone-map-label",
        html: `<div class="zone-pill ${isSelected ? "active" : ""}" style="--zone-color:${zone.color}">
                 ${zone.name}
               </div>`,
        iconSize: [110, 32],
        iconAnchor: [55, 16]
      });
      L.marker(zone.center, { icon: zoneBadge, interactive: false }).addTo(map);

      poly.on("mouseover", () => {
        poly.setStyle({
          fillOpacity: 0.48,
          weight: 3.5,
          color: "#fde047"
        });
      });

      poly.on("mouseout", () => {
        poly.setStyle({
          fillOpacity: isSelected ? 0.42 : 0.18,
          weight: isSelected ? 3.5 : 2,
          color: "#ffffff"
        });
      });

      // Un solo clic selecciona la zona y cierra el modal inmediatamente
      poly.on("click", () => {
        onSelectRegion(zone.id);
      });
    });

    // 3. Contorno provincial de San Luis bien marcado
    const provinceLayer = L.polygon(SAN_LUIS_PROVINCE_BORDER, {
      color: "#ffffff",
      weight: 3,
      fill: false,
      interactive: false
    }).addTo(map);

    mapRef.current = map;

    setTimeout(() => {
      map.invalidateSize();
      // Zoom inicial más cercano ocupando casi todo el alto del contenedor
      map.fitBounds(provinceLayer.getBounds(), { padding: [4, 4] });
      map.setZoom(Math.max(map.getZoom(), 7.25));
      syncZoomVisibility();
    }, 50);

    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="region-modal-overlay" onClick={onClose}>
      <div className="region-modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="region-modal-header">
          <div>
            <h3>🛰️ Seleccioná tu zona en San Luis</h3>
            <p>Hacé clic en Norte, Centro o Sur · Acercá el zoom para ver ciudades y localidades</p>
          </div>
          <button type="button" className="region-modal-close" onClick={onClose} aria-label="Cerrar">
            ✕
          </button>
        </div>

        <div className="region-leaflet-container" ref={containerRef} />
      </div>
    </div>
  );
}

export { SAN_LUIS_ZONES as SAN_LUIS_REGIONS };
