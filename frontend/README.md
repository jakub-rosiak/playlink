# Frontend — SvelteKit

SvelteKit-based frontend for the Playlink project.

## Requirements

- **Node.js 22.x** (or later)
- **pnpm** (Recommended package manager)

## Technologies Used

- **Svelte** `^5.51.0` (latest)
- **SvelteKit** `^2.50.2`
- **Vite** `^7.x`
- **adapter-node** (For production-ready Docker hosting)

## Getting Started

### 1. Installation

Install dependencies:

```bash
cd frontend
pnpm install
```

### 2. Running the Dev Server

Start the development server with Hot Module Replacement (HMR):

```bash
pnpm dev

# or open in browser automatically
pnpm dev -- --open
```

The app will be available at `http://localhost:5173/` (or the port shown in your terminal).

### 3. Docker Deployment

To build and run the frontend standalone in a container:

```bash
docker build -t frontend-playlink .
docker run -p 3000:3000 frontend-playlink
```

The containerized app will be available at `http://localhost:3000`.

### 4. Building for Production (Manual)

```bash
pnpm run build
```

Output is placed under the `build/` directory (configured via `adapter-node`).

## Project Structure

```
frontend/
├── src/
│   ├── lib/             # Shared Svelte components and utilities
│   │   └── index.js     # Public exports
│   ├── routes/          # SvelteKit file-based routing
│   │   ├── +layout.svelte  # Root layout
│   │   ├── +page.svelte    # Home page
│   │   └── test/           # Backend interaction test page
│   │       └── +page.svelte
│   └── app.html         # HTML shell
├── static/              # Static assets served as-is
├── jsconfig.json
├── package.json
├── pnpm-lock.yaml       # pnpm lockfile
├── Dockerfile           # Container configuration
├── svelte.config.js     # SvelteKit + Svelte configuration
└── vite.config.js
```

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte extension](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

## Notes

- This project uses **Svelte 5 runes** (`$state`, `$derived`, `$props`, etc.).
- **Backend Interaction**: The `/test` page demonstrates how to fetch data from the FastAPI backend. Ensure the backend is running and CORS is properly configured.
- **Adapter**: This project is configured with `@sveltejs/adapter-node` for standard Node.js server deployments and Docker compatibility.
