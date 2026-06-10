function highlightTimelineItem(eventId) {
    document.querySelectorAll('.event-item').forEach(el => {
        el.classList.remove('highlighted');
        if (parseInt(el.dataset.id) === eventId) {
            el.classList.add('highlighted');
            el.style.borderLeftColor = '';
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
}

const TimelineModule = {
    init(events, onEventClick) {
        this.events = events;
        this.onEventClick = onEventClick;
        this.render();
    },

    render(filteredEvents) {
        const container = document.getElementById('event-list');
        const events = filteredEvents || this.events;

        const sorted = [...events].sort((a, b) =>
            new Date(b.event_time) - new Date(a.event_time)
        );

        container.innerHTML = sorted.map(event => {
            const drug = CONFIG.drugTypes[event.drug_type] || CONFIG.drugTypes.other;
            const cat = CONFIG.categories[event.category] || CONFIG.categories.seizure;
            const date = new Date(event.event_time).toLocaleDateString('en-GB', {
                day: 'numeric', month: 'short', year: 'numeric'
            });
            const time = new Date(event.event_time).toLocaleTimeString('en-GB', {
                hour: '2-digit', minute: '2-digit'
            });

            return `
                <div class="event-item" data-id="${event.id}"
                     style="border-left-color:${cat.color}">
                    <div class="event-time">${date} · ${time}</div>
                    <div class="event-title">${event.title}</div>
                    <div class="event-meta">
                        <span class="event-tag" style="background:${cat.color}22;color:${cat.color}">
                            ${cat.icon} ${cat.label}
                        </span>
                        <span class="event-tag" style="background:${drug.color}22;color:${drug.color === '#f9fafb' ? '#888' : drug.color}">
                            ${drug.icon} ${drug.label}
                        </span>
                        ${event.quantity_kg ? `<span class="event-tag">${event.quantity_kg.toLocaleString()} kg</span>` : ''}
                    </div>
                    <div class="event-location">📍 ${event.city}, ${event.country}</div>
                </div>
            `;
        }).join('');

        container.querySelectorAll('.event-item').forEach(el => {
            el.addEventListener('click', () => {
                const id = parseInt(el.dataset.id);
                this.onEventClick(id);
            });
        });

        this.updateStats(events);
    },

    updateStats(events) {
        document.getElementById('stat-total').textContent = events.length;
        const countries = new Set(events.map(e => e.country));
        document.getElementById('stat-countries').textContent = countries.size;
        const totalKg = events.reduce((sum, e) => sum + (e.quantity_kg || 0), 0);
        document.getElementById('stat-seizures').textContent = totalKg.toLocaleString();
    }
};
