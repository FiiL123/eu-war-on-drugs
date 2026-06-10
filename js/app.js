let map;
let currentEvents = [];

document.addEventListener('DOMContentLoaded', async () => {
    map = L.map('map', {
        center: CONFIG.map.center,
        zoom: CONFIG.map.zoom,
        minZoom: CONFIG.map.minZoom,
        maxZoom: CONFIG.map.maxZoom,
        zoomControl: true
    });

    L.tileLayer(CONFIG.map.tileLayer, {
        attribution: CONFIG.map.attribution,
        maxZoom: 18
    }).addTo(map);

    const apiData = await ApiModule.getEvents();
    currentEvents = apiData || SAMPLE_EVENTS;

    MarkersModule.addEvents(map, currentEvents);

    FiltersModule.init(currentEvents, (disabledDrugTypes, disabledCategories) => {
        MarkersModule.filterByExcluded(disabledDrugTypes, disabledCategories);
        const filtered = FiltersModule.getFilteredEvents();
        TimelineModule.render(filtered);
    });

    TimelineModule.init(currentEvents, (eventId) => {
        MarkersModule.panToEvent(map, eventId);
    });

    setTimeout(() => map.invalidateSize(), 100);
});
