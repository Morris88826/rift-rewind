# Rift Rewind - League of Legends Stats Tracker

A Vue.js application for tracking League of Legends player statistics and year-end highlights.

**Live Site**: https://morris88826.github.io/rift-rewind/

## Features

- 📅 **Calendar View** - Browse match history in a calendar layout
- 📊 **Infographic** - Visual performance analysis with radar charts comparing your stats to average
- 👑 **Mastery System** - NBA 2K-style champion mastery cards with achievement badges
- 📈 **Progression Charts** - Track mastery progression over time
- 🎯 **Performance Analytics** - Detailed statistics by champion, lane, and game mode

## Project Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```sh
npm install
```

### Development

```sh
npm run dev
```

Runs the app in development mode with hot reload.

### Production Build

```sh
npm run build
```

Builds the project for production to the `dist/` folder.

### Preview Production Build

```sh
npm run preview
```

## Deployment

This project is automatically deployed to GitHub Pages on every push to the main branch using GitHub Actions.

### Automatic Deployment
- The workflow file is located in `.github/workflows/deploy.yml`
- Triggers on push to `main` or `master` branch
- Builds the project and deploys to GitHub Pages automatically

### Manual Deployment
```sh
npm run build
# The dist/ folder is ready for deployment to GitHub Pages
```

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── ChatWidget.vue
│   ├── FeatureCard.vue
│   └── MatchStoryModal.vue
├── views/              # Page components
│   ├── HomeView.vue
│   ├── RewindView.vue
│   ├── CalendarView.vue
│   ├── InfographicView.vue
│   ├── MasteryView.vue
│   └── AboutView.vue
├── router/
│   └── index.js        # Vue Router configuration
├── App.vue             # Root component
└── main.js             # Application entry point
```

## Routes

- `/` - Home page
- `/rewind/:riotId/:region` - Rewind stats page with feature cards
- `/rewind/:riotId/:region/calendar` - Calendar view of match history
- `/rewind/:riotId/:region/infographic` - Performance infographic with radar charts
- `/rewind/:riotId/:region/mastery` - Champion mastery achievements
- `/about` - About page

## Technologies

- **Vue 3** - Progressive JavaScript framework
- **Vue Router 4** - Client-side routing
- **Chart.js** - Data visualization library
- **Vite** - Fast build tool and development server

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur)

## Recommended Browser Setup

- Chromium-based browsers: [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
- Firefox: [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

## License

This project is open source and available under the MIT License.

## Author

Morris - GitHub: [@Morris88826](https://github.com/Morris88826)
