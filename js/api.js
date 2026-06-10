const ApiModule = {
    baseUrl: CONFIG.apiBaseUrl,

    async getEvents(params = {}) {
        try {
            const url = new URL(`${this.baseUrl}/events`);
            Object.entries(params).forEach(([key, val]) => {
                if (val) url.searchParams.set(key, val);
            });
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (err) {
            console.warn('API unavailable, using sample data:', err.message);
            return null;
        }
    },

    async getEvent(id) {
        try {
            const response = await fetch(`${this.baseUrl}/events/${id}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (err) {
            console.warn('API unavailable');
            return null;
        }
    }
};
