// Leaflet карта для Fitness Competition Mini App

class FitnessMap {
    constructor() {
        this.map = null;
        this.userMarker = null;
        this.routePolyline = null;
        this.userLocation = null;
        this.routePoints = [];
        this.totalDistance = 0;

        this.init();
    }

    init() {
        // Ініціалізація карти після завантаження DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initializeMap();
            });
        } else {
            this.initializeMap();
        }
    }

    initializeMap() {
        const mapElement = document.getElementById('leaflet-map');
        if (!mapElement) {
            console.error('Map element not found');
            return;
        }

        // Створення екземпляру карти
        this.map = L.map('leaflet-map', {
            zoomControl: true,
            attributionControl: false
        }).setView([50.4501, 30.5234], 13); // Київ за замовчуванням

        // Додавання тайлового шару OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Спроба отримати поточну локацію
        this.getCurrentLocation();

        // Налаштування обробників подій
        this.setupMapEvents();

        // Збереження глобального посилання
        window.mapInstance = this.map;
        window.updateMapLocation = (lat, lng) => this.updateUserLocation(lat, lng);

        console.log('🗺️ Карта ініціалізована');
    }

    getCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    this.updateUserLocation(latitude, longitude);
                    this.map.setView([latitude, longitude], 16);
                },
                (error) => {
                    console.warn('Геолокація недоступна:', error.message);
                    // Використовуємо Київ як fallback
                    this.updateUserLocation(50.4501, 30.5234);
                }
            );
        }
    }

    updateUserLocation(lat, lng) {
        this.userLocation = [lat, lng];

        // Оновлення маркера користувача
        if (this.userMarker) {
            this.userMarker.setLatLng([lat, lng]);
        } else {
            // Створення нового маркера
            this.userMarker = L.marker([lat, lng], {
                icon: this.createUserIcon()
            }).addTo(this.map);

            this.userMarker.bindPopup('📍 Ваша позиція').openPopup();
        }

        // Додавання точки до маршруту
        this.addRoutePoint(lat, lng);

        // Оновлення статистики
        this.updateDistanceStats();
    }

    createUserIcon() {
        return L.icon({
            iconUrl: 'data:image/svg+xml;base64,' + btoa(`
                <svg width="32" height="32" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="16" cy="16" r="8" fill="#0088cc" stroke="#ffffff" stroke-width="2"/>
                    <circle cx="16" cy="16" r="4" fill="#ffffff"/>
                </svg>
            `),
            iconSize: [32, 32],
            iconAnchor: [16, 16],
            popupAnchor: [0, -16]
        });
    }

    addRoutePoint(lat, lng) {
        const newPoint = [lat, lng];
        this.routePoints.push(newPoint);

        // Обмеження кількості точок для продуктивності
        if (this.routePoints.length > 100) {
            this.routePoints = this.routePoints.slice(-50);
        }

        this.updateRoutePolyline();
    }

    updateRoutePolyline() {
        if (this.routePoints.length < 2) return;

        // Видалення старого маршруту
        if (this.routePolyline) {
            this.map.removeLayer(this.routePolyline);
        }

        // Створення нового маршруту
        this.routePolyline = L.polyline(this.routePoints, {
            color: '#ff6b35',
            weight: 4,
            opacity: 0.8,
            smoothFactor: 1
        }).addTo(this.map);
    }

    calculateDistance(point1, point2) {
        // Формула гаверсинуса для розрахунку відстані між двома точками
        const R = 6371; // Радіус Землі в км
        const dLat = this.toRadians(point2[0] - point1[0]);
        const dLon = this.toRadians(point2[1] - point1[1]);

        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(this.toRadians(point1[0])) * Math.cos(this.toRadians(point2[0])) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // Відстань в км
    }

    toRadians(degrees) {
        return degrees * (Math.PI / 180);
    }

    updateDistanceStats() {
        if (this.routePoints.length < 2) return;

        // Розрахунок загальної відстані
        let totalDistance = 0;
        for (let i = 1; i < this.routePoints.length; i++) {
            totalDistance += this.calculateDistance(
                this.routePoints[i - 1], 
                this.routePoints[i]
            );
        }

        this.totalDistance = totalDistance;

        // Оновлення UI
        const sessionDistanceElement = document.getElementById('session-distance');
        if (sessionDistanceElement) {
            sessionDistanceElement.textContent = `${totalDistance.toFixed(2)} км`;
        }
    }

    setupMapEvents() {
        // Обробник кліку по карті
        this.map.on('click', (e) => {
            const { lat, lng } = e.latlng;
            console.log(`Клік по карті: ${lat.toFixed(6)}, ${lng.toFixed(6)}`);
        });

        // Обробник зміни масштабу
        this.map.on('zoomend', () => {
            console.log(`Масштаб змінено на: ${this.map.getZoom()}`);
        });
    }

    clearRoute() {
        this.routePoints = [];
        this.totalDistance = 0;

        if (this.routePolyline) {
            this.map.removeLayer(this.routePolyline);
            this.routePolyline = null;
        }

        // Оновлення UI
        const sessionDistanceElement = document.getElementById('session-distance');
        if (sessionDistanceElement) {
            sessionDistanceElement.textContent = '0 км';
        }
    }

    centerOnUser() {
        if (this.userLocation) {
            this.map.setView(this.userLocation, 16);
        }
    }
}

// Ініціалізація карти
window.fitnessMap = new FitnessMap();