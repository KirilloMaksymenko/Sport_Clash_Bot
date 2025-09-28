// Основна JavaScript логіка для Fitness Competition Mini App

class FitnessApp {
    constructor() {
        this.tg = window.Telegram.WebApp;
        this.currentTab = 'home';
        this.isTracking = false;
        this.activeCompetition = null;
        this.userStats = {
            totalDistance: 0,
            totalSteps: 0,
            currentRank: 'bronze',
            totalPoints: 0
        };

        this.init();
    }

    init() {
        // Ініціалізація Telegram Mini App
        this.tg.ready();
        this.tg.expand();

        // Налаштування теми
        this.setupTheme();

        // Налаштування обробників подій
        this.setupEventListeners();

        // Завантаження даних користувача
        this.loadUserData();

        console.log('🚀 Fitness App ініціалізовано');
    }

    setupTheme() {
        // Використання кольорів теми Telegram
        const root = document.documentElement;

        if (this.tg.themeParams) {
            root.style.setProperty('--tg-theme-bg-color', this.tg.themeParams.bg_color || '#ffffff');
            root.style.setProperty('--tg-theme-text-color', this.tg.themeParams.text_color || '#000000');
            root.style.setProperty('--tg-theme-button-color', this.tg.themeParams.button_color || '#0088cc');
        }
    }

    setupEventListeners() {
        // Навігація по вкладках
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Кнопки відстеження
        document.getElementById('start-tracking')?.addEventListener('click', () => {
            this.startTracking();
        });

        document.getElementById('stop-tracking')?.addEventListener('click', () => {
            this.stopTracking();
        });

        // Фільтри рейтингу
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterRankings(e.target.dataset.filter);
            });
        });

        // Кнопки карти
        document.getElementById('center-location')?.addEventListener('click', () => {
            this.centerMapOnLocation();
        });

        document.getElementById('show-route')?.addEventListener('click', () => {
            this.showRoute();
        });
    }

    switchTab(tabName) {
        // Зміна активної вкладки
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;

        // Оновлення контенту залежно від вкладки
        if (tabName === 'rankings') {
            this.loadRankings();
        } else if (tabName === 'competitions') {
            this.loadCompetitions();
        } else if (tabName === 'map') {
            setTimeout(() => {
                if (window.mapInstance) {
                    window.mapInstance.invalidateSize();
                }
            }, 100);
        }
    }

    startTracking() {
        this.isTracking = true;
        document.getElementById('start-tracking').disabled = true;
        document.getElementById('stop-tracking').disabled = false;

        // Запит дозволу на геолокацію
        if (navigator.geolocation) {
            this.watchId = navigator.geolocation.watchPosition(
                (position) => {
                    this.handleLocationUpdate(position);
                },
                (error) => {
                    console.error('Помилка геолокації:', error);
                    this.showNotification('Помилка', 'Не вдалося отримати доступ до геолокації');
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        }

        this.showNotification('Відстеження розпочато', '📍 GPS відстеження активовано!');
    }

    stopTracking() {
        this.isTracking = false;
        document.getElementById('start-tracking').disabled = false;
        document.getElementById('stop-tracking').disabled = true;

        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
        }

        this.showNotification('Відстеження зупинено', '⏹️ GPS відстеження деактивовано.');
    }

    handleLocationUpdate(position) {
        const { latitude, longitude, speed } = position.coords;

        // Оновлення карти
        if (window.updateMapLocation) {
            window.updateMapLocation(latitude, longitude);
        }

        // Оновлення швидкості
        const speedKmh = speed ? (speed * 3.6).toFixed(1) : '0';
        const speedElement = document.getElementById('current-speed');
        if (speedElement) {
            speedElement.textContent = `${speedKmh} км/год`;
        }

        // Надсилання даних до бота
        this.sendLocationToBot(latitude, longitude);

        console.log(`📍 Локація оновлена: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`);
    }

    sendLocationToBot(latitude, longitude) {
        // Надсилання даних через Telegram Mini App API
        const locationData = {
            latitude,
            longitude,
            timestamp: Date.now(),
            user_id: this.tg.initDataUnsafe.user?.id
        };

        // Відправка даних до бота
        this.tg.sendData(JSON.stringify({
            type: 'location_update',
            data: locationData
        }));
    }

    loadUserData() {
        // Симуляція завантаження даних користувача
        setTimeout(() => {
            this.userStats = {
                totalDistance: 12.5,
                totalSteps: 8420,
                currentRank: 'silver',
                totalPoints: 245
            };

            this.updateStatsDisplay();
        }, 1000);
    }

    updateStatsDisplay() {
        const elements = {
            'total-distance': `${this.userStats.totalDistance} км`,
            'total-steps': this.userStats.totalSteps.toLocaleString(),
            'total-points': this.userStats.totalPoints
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });

        const rankEmojis = {
            bronze: '🥉',
            silver: '🥈', 
            gold: '🥇',
            platinum: '💎',
            diamond: '👑'
        };

        const rankElement = document.getElementById('current-rank');
        if (rankElement) {
            rankElement.textContent = rankEmojis[this.userStats.currentRank] || '🥉';
        }
    }

    loadRankings() {
        const leaderboard = document.getElementById('leaderboard');
        if (!leaderboard) return;

        // Симуляція даних лідерборду
        const mockLeaders = [
            { rank: 1, name: 'Олександр М.', points: 1250, level: '🥇' },
            { rank: 2, name: 'Марія К.', points: 1180, level: '🥈' },
            { rank: 3, name: 'Іван П.', points: 980, level: '🥉' },
            { rank: 4, name: 'Анна С.', points: 876, level: '🏃‍♀️' },
            { rank: 5, name: 'Петро Л.', points: 654, level: '🏃‍♂️' }
        ];

        leaderboard.innerHTML = mockLeaders.map(leader => `
            <div class="leader-item">
                <div class="leader-rank">#${leader.rank}</div>
                <div class="leader-info">
                    <div class="leader-name">${leader.name}</div>
                    <div class="leader-details">${leader.level} Активний гравець</div>
                </div>
                <div class="leader-points">${leader.points} очок</div>
            </div>
        `).join('');
    }

    filterRankings(filter) {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        const activeBtn = document.querySelector(`[data-filter="${filter}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }

        // Перезавантаження рейтингу з новим фільтром
        this.loadRankings();
    }

    loadCompetitions() {
        // Завантаження активних змагань
        console.log('🏆 Завантаження списку змагань');
    }

    startCompetition(type) {
        this.activeCompetition = {
            type: type,
            startTime: Date.now(),
            duration: type === 'sprint' ? 30 : 90 // хвилин
        };

        const activeCompElement = document.getElementById('active-competition');
        const compTypeElement = document.getElementById('comp-type');
        const compPositionElement = document.getElementById('comp-position');

        if (activeCompElement) {
            activeCompElement.style.display = 'block';
        }
        if (compTypeElement) {
            compTypeElement.textContent = type === 'sprint' ? 'Sprint забіг ⚡' : 'Endurance забіг 🏃‍♂️';
        }
        if (compPositionElement) {
            compPositionElement.textContent = '1-е місце';
        }

        this.startCompetitionTimer();
        this.showNotification('Змагання розпочато!', `🏆 ${type === 'sprint' ? 'Sprint' : 'Endurance'} забіг активовано!`);
    }

    startCompetitionTimer() {
        if (!this.activeCompetition) return;

        this.competitionInterval = setInterval(() => {
            const elapsed = Date.now() - this.activeCompetition.startTime;
            const remaining = (this.activeCompetition.duration * 60 * 1000) - elapsed;

            if (remaining <= 0) {
                this.finishCompetition();
                return;
            }

            const minutes = Math.floor(remaining / (60 * 1000));
            const seconds = Math.floor((remaining % (60 * 1000)) / 1000);

            const timerElement = document.getElementById('comp-timer');
            if (timerElement) {
                timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }

    finishCompetition() {
        if (this.competitionInterval) {
            clearInterval(this.competitionInterval);
        }

        const activeCompElement = document.getElementById('active-competition');
        if (activeCompElement) {
            activeCompElement.style.display = 'none';
        }
        this.activeCompetition = null;

        this.showNotification('Змагання завершено!', '🎉 Вітаємо! Ви завершили змагання.');
    }

    showNotification(title, message) {
        // Використання Telegram haptic feedback
        if (this.tg.HapticFeedback) {
            this.tg.HapticFeedback.notificationOccurred('success');
        }

        // Показ повідомлення через Telegram
        if (this.tg.showPopup) {
            this.tg.showPopup({
                title: title,
                message: message
            });
        } else {
            alert(`${title}: ${message}`);
        }
    }

    centerMapOnLocation() {
        if (navigator.geolocation && window.mapInstance) {
            navigator.geolocation.getCurrentPosition((position) => {
                window.mapInstance.setView([position.coords.latitude, position.coords.longitude], 16);
            });
        }
    }

    showRoute() {
        this.showNotification('Маршрут', '🛣️ Функція відображення маршруту активна');
    }
}

// Ініціалізація додатку після завантаження DOM
document.addEventListener('DOMContentLoaded', () => {
    window.fitnessApp = new FitnessApp();
});

// Глобальні функції для використання в HTML
window.startCompetition = (type) => {
    if (window.fitnessApp) {
        window.fitnessApp.startCompetition(type);
    }
};