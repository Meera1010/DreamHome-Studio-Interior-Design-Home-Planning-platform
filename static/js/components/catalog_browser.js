/**
 * DreamHome Studio — Catalog Browser Drawer Component Controller
 */

window.DHCatalogBrowser = {
    async loadCatalog(containerId, canvasEngine, category = null) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '<div style="padding:1rem;color:var(--text-muted);">Loading catalog...</div>';

        try {
            const data = await DHAPIClient.getFurniture(category);
            const items = data.furniture || [];

            if (items.length === 0) {
                container.innerHTML = '<div style="padding:1rem;color:var(--text-muted);">No catalog items found.</div>';
                return;
            }

            container.innerHTML = items.map(item => `
                <div class="catalog-card" data-id="${item.id}">
                    <img src="${item.thumbnail_url || '/static/images/catalog/default.svg'}" alt="${item.name}" onerror="this.src='/static/images/catalog/default.svg'">
                    <div class="catalog-item-name">${item.name}</div>
                    <div class="catalog-item-price">$${item.price.toLocaleString()}</div>
                    <button class="btn btn-outline btn-sm add-btn" style="width:100%;margin-top:0.4rem;">Add to Room</button>
                </div>
            `).join('');

            // Bind Add to Canvas Click Listeners
            container.querySelectorAll('.catalog-card').forEach((card, index) => {
                const addBtn = card.querySelector('.add-btn');
                const catalogItem = items[index];

                addBtn.addEventListener('click', () => {
                    if (canvasEngine) {
                        const newObj = DHObjectManager.createFurnitureObject(catalogItem, 250, 200);
                        canvasEngine.objects.push(newObj);
                        canvasEngine.selectedObject = newObj;
                        canvasEngine.requestRender();
                        if (window.DHToast) window.DHToast.success(`Added ${catalogItem.name}`);
                    }
                });
            });

        } catch (err) {
            container.innerHTML = '<div style="padding:1rem;color:var(--danger);">Failed to load catalog items.</div>';
        }
    }
};
