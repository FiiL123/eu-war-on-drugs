const FiltersModule = {
    disabledDrugTypes: new Set(),
    disabledCategories: new Set(),

    init(events, onFilterChange) {
        this.events = events;
        this.onFilterChange = onFilterChange;
        this.renderDrugFilters();
        this.renderCategoryFilters();
        this.renderLegend();
    },

    renderDrugFilters() {
        const container = document.getElementById('drug-filters');
        const usedTypes = [...new Set(this.events.map(e => e.drug_type))];

        container.innerHTML = '';
        usedTypes.forEach(type => {
            const config = CONFIG.drugTypes[type];
            if (!config) return;
            const btn = document.createElement('button');
            btn.className = 'filter-btn active';
            btn.dataset.type = type;
            btn.innerHTML = `<span class="dot" style="background:${config.color}"></span>${config.label}`;
            btn.addEventListener('click', () => {
                if (this.disabledDrugTypes.has(type)) {
                    this.disabledDrugTypes.delete(type);
                    btn.classList.add('active');
                } else {
                    this.disabledDrugTypes.add(type);
                    btn.classList.remove('active');
                }
                this.applyFilters();
            });
            container.appendChild(btn);
        });
    },

    renderCategoryFilters() {
        const container = document.getElementById('category-filters');
        const usedCats = [...new Set(this.events.map(e => e.category))];

        container.innerHTML = '';
        usedCats.forEach(cat => {
            const config = CONFIG.categories[cat];
            if (!config) return;
            const btn = document.createElement('button');
            btn.className = 'filter-btn active';
            btn.dataset.category = cat;
            btn.innerHTML = `<span class="dot" style="background:${config.color}"></span>${config.label}`;
            btn.addEventListener('click', () => {
                if (this.disabledCategories.has(cat)) {
                    this.disabledCategories.delete(cat);
                    btn.classList.add('active');
                } else {
                    this.disabledCategories.add(cat);
                    btn.classList.remove('active');
                }
                this.applyFilters();
            });
            container.appendChild(btn);
        });
    },

    renderLegend() {
        const drugContainer = document.getElementById('legend-items');
        const catContainer = document.getElementById('legend-categories');

        const usedTypes = [...new Set(this.events.map(e => e.drug_type))];
        const usedCats = [...new Set(this.events.map(e => e.category))];

        drugContainer.innerHTML = usedTypes.map(type => {
            const c = CONFIG.drugTypes[type];
            return `<div class="legend-item"><span class="legend-dot" style="background:${c.color}"></span>${c.label}</div>`;
        }).join('');

        catContainer.innerHTML = usedCats.map(cat => {
            const c = CONFIG.categories[cat];
            return `<div class="legend-item"><span class="legend-dot" style="background:${c.color}"></span>${c.label}</div>`;
        }).join('');
    },

    applyFilters() {
        this.onFilterChange(this.disabledDrugTypes, this.disabledCategories);
    },

    getFilteredEvents() {
        return this.events.filter(event => {
            return !this.disabledDrugTypes.has(event.drug_type) && !this.disabledCategories.has(event.category);
        });
    }
};
