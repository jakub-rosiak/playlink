# Frontend — Svelte

Svelte-based frontend for the Playlink project.

## Requirements

- **Node.js 20.11.0 LTS** (or later)
- **npm**

## Technologies Used

- **Svelte** `4.2.9`
- **Vite** `^5.4.x`
- **@sveltejs/vite-plugin-svelte** `^3.1.x`

## Getting Started

### 1. Installation

Install dependencies:

```bash
cd frontend
npm install
```

### 2. Running the Dev Server

Start the development server with Hot Module Replacement (HMR):

```bash
npm run dev
```

The app will be available at `http://localhost:5173/`

### 3. Building for Production

```bash
npm run build
```

The production-ready files will be output to `dist/`.

### 4. Previewing the Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/          # Static assets served as-is
├── src/
│   ├── assets/      # Images, SVGs and other media
│   ├── lib/         # Reusable Svelte components
│   ├── App.svelte   # Root application component
│   ├── app.css      # Global styles
│   └── main.js      # Application entry point
├── index.html       # HTML entry point
├── package.json
├── svelte.config.js
└── vite.config.js
```

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte extension](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

## Notes

- This project uses **Svelte 4** (not SvelteKit). For server-side rendering or
  advanced routing, consider migrating to [SvelteKit](https://kit.svelte.dev/).
- State management uses standard Svelte 4 reactive declarations (`let`, `$:`).
  The Svelte 5 runes API (`$state`, `$derived`, etc.) is **not** used here.
- HMR state preservation is disabled by default. For persistent state, use
  [Svelte stores](https://svelte.dev/docs/svelte-store).

