function createMarkerIcon(drugType, category, isRecent) {
    const drug = CONFIG.drugTypes[drugType] || CONFIG.drugTypes.other;
    const cat = CONFIG.categories[category] || CONFIG.categories.seizure;
    const size = isRecent ? 40 : 32;
    const iconSize = 16;

    const pinHtml = `
        <svg width="${size}" height="${size + 12}" viewBox="0 0 ${size} ${size + 12}" xmlns="http://www.w3.org/2000/svg">
            <path d="M${size/2} ${size + 11} C${size/2} ${size + 11} ${2} ${size * 0.6} ${2} ${size * 0.38}
                     C${2} ${size * 0.17} ${size * 0.17} 2 ${size/2} 2
                     C${size * 0.83} 2 ${size - 2} ${size * 0.17} ${size - 2} ${size * 0.38}
                     C${size - 2} ${size * 0.6} ${size/2} ${size + 11} ${size/2} ${size + 11}Z"
                fill="${drug.color}" stroke="#fff" stroke-width="1.5"
                style="filter:drop-shadow(0 2px 4px rgba(0,0,0,0.3))${isRecent ? ';animation:pinPulse 2s infinite' : ''}"/>
            <g transform="translate(${size/2 - iconSize/2}, ${size * 0.18}) scale(${iconSize / 24})">
                ${cat.svg}
            </g>
        </svg>
    `;

    return L.divIcon({
        className: 'custom-marker' + (isRecent ? ' marker-pulse' : ''),
        html: pinHtml,
        iconSize: [size, size + 12],
        iconAnchor: [size / 2, size + 12],
        popupAnchor: [0, -(size + 12)]
    });
}

function createPopupContent(event) {
    const drug = CONFIG.drugTypes[event.drug_type] || CONFIG.drugTypes.other;
    const cat = CONFIG.categories[event.category] || CONFIG.categories.seizure;
    const date = new Date(event.event_time).toLocaleDateString('en-GB', {
        day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });

    let html = `
        <div class="popup-title">${event.title}</div>
        <div class="popup-meta">
            ${cat.icon} ${cat.label} · ${drug.icon} ${drug.label}<br>
            📍 ${event.city}, ${event.country} · ${date}
        </div>
    `;
    if (event.quantity_kg) {
        html += `<div class="popup-meta" style="margin-top:4px;">⚖️ ${event.quantity_kg.toLocaleString()} kg seized</div>`;
    }
    if (event.source_url) {
        html += `<a href="${event.source_url}" target="_blank" class="popup-link">Source: ${event.source_name}</a>`;
    }

    return html;
}

const MarkersModule = {
    markers: [],
    markerCluster: null,

    addEvents(map, events) {
        this.clearAll();

        events.forEach(event => {
            const isRecent = (Date.now() - new Date(event.event_time).getTime()) < 48 * 60 * 60 * 1000;
            const icon = createMarkerIcon(event.drug_type, event.category, isRecent);
            const marker = L.marker([event.lat, event.lng], { icon });

            marker.eventData = event;

            marker.bindPopup(createPopupContent(event), {
                maxWidth: 280,
                className: 'custom-popup'
            });

            marker.on('click', () => {
                highlightTimelineItem(event.id);
            });

            marker.addTo(map);
            this.markers.push(marker);
        });
    },

    clearAll() {
        this.markers.forEach(m => m.remove());
        this.markers = [];
    },

    filterByExcluded(disabledDrugTypes, disabledCategories) {
        this.markers.forEach(marker => {
            const event = marker.eventData;
            const hidden = disabledDrugTypes.has(event.drug_type) || disabledCategories.has(event.category);

            if (hidden) {
                marker.setOpacity(0.12);
                marker.getElement().style.pointerEvents = 'none';
            } else {
                marker.setOpacity(1);
                marker.getElement().style.pointerEvents = '';
            }
        });
    },

    showOnly(ids) {
        this.markers.forEach(marker => {
            const event = marker.eventData;
            if (ids === null || ids.includes(event.id)) {
                marker.setOpacity(1);
            } else {
                marker.setOpacity(0.15);
            }
        });
    },

    panToEvent(map, eventId) {
        const marker = this.markers.find(m => m.eventData.id === eventId);
        if (marker) {
            map.setView([marker.eventData.lat, marker.eventData.lng], 8, { animate: true });
            marker.openPopup();
        }
    }
};
