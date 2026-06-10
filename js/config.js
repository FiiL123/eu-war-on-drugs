const CONFIG = {
    map: {
        center: [50.0, 15.0],
        zoom: 5,
        minZoom: 3,
        maxZoom: 18,
        tileLayer: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>'
    },
    drugTypes: {
        cocaine:  { color: '#e5e7eb', label: 'Cocaine',   icon: '🤍' },
        heroin:   { color: '#b45309', label: 'Heroin',    icon: '🟤' },
        cannabis: { color: '#16a34a', label: 'Cannabis',  icon: '🌿' },
        synthetic:{ color: '#a855f7', label: 'Synthetic', icon: '🟣' },
        fentanyl: { color: '#ef4444', label: 'Fentanyl',  icon: '🔴' },
        mdma:     { color: '#f59e0b', label: 'MDMA',      icon: '🟡' },
        other:    { color: '#6b7280', label: 'Other',     icon: '⚪' }
    },
    categories: {
        seizure:          { color: '#ef4444', label: 'Seizure',           icon: '📦', svg: '<path d="M3 7h18v13H3z M6 7V5a6 6 0 0 1 12 0v2" stroke="white" stroke-width="2" fill="none"/>' },
        arrest:           { color: '#f59e0b', label: 'Arrest',            icon: '🚔', svg: '<circle cx="12" cy="6" r="3" stroke="white" stroke-width="2" fill="none"/><path d="M7 21v-2a5 5 0 0 1 10 0v2" stroke="white" stroke-width="2" fill="none"/>' },
        lab_bust:         { color: '#a855f7', label: 'Lab Bust',          icon: '🔬', svg: '<path d="M9 3v7L5 19h14l-4-9V3 M7 3h10" stroke="white" stroke-width="2" fill="none"/>' },
        port_interdiction:{ color: '#06b6d4', label: 'Port Interdiction', icon: '🚢', svg: '<path d="M3 17l3-7h12l3 7 M6 10V6h12v4 M9 6V3h6v3" stroke="white" stroke-width="2" fill="none"/>' },
        dark_web:         { color: '#6366f1', label: 'Dark Web Bust',    icon: '🌐', svg: '<circle cx="12" cy="12" r="9" stroke="white" stroke-width="2" fill="none"/><ellipse cx="12" cy="12" rx="4" ry="9" stroke="white" stroke-width="1.5" fill="none"/><path d="M3 12h18" stroke="white" stroke-width="1.5"/>' },
        overdose:         { color: '#dc2626', label: 'Overdose Cluster',  icon: '⚠️', svg: '<path d="M12 3L2 20h20z" stroke="white" stroke-width="2" fill="none"/><path d="M12 10v4 M12 16.5v1" stroke="white" stroke-width="2.5" stroke-linecap="round"/>' },
        policy:           { color: '#10b981', label: 'Policy Change',     icon: '📋', svg: '<path d="M6 3h9l5 5v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" stroke="white" stroke-width="2" fill="none"/><path d="M8 13h8 M8 17h5" stroke="white" stroke-width="2" stroke-linecap="round"/>' },
        route:            { color: '#3b82f6', label: 'Trafficking Route', icon: '➡️', svg: '<path d="M5 12h14 M15 7l5 5-5 5" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' }
    },
    apiBaseUrl: 'http://localhost:8000'
};
