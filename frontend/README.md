# Frontend — SvelteKit

SvelteKit-based frontend for the Playlink project. Implements the BIP39 sign-in flow and the rooms browser, talking to the FastAPI backend over REST and WebSockets.

## Requirements

- **Bun** (latest)

## Tech Stack

- **Svelte** `^5.51.0` (runes mode: `$state`, `$derived`, `$effect`, `$props`)
- **SvelteKit** `^2.50.2` with `@sveltejs/adapter-node`
- **TypeScript** (strict)
- **Bun** — runtime, package manager, bundler
- **ethers** + **viem** — local mnemonic derivation and ECDSA signing
- **jwt-decode** — server-side decoding of the session cookie

## Getting Started

> Use **Bun only** for dependency management and scripts in this project.
> Do not use `npm`, `pnpm`, or `yarn`.

### 1. Installation

```bash
cd frontend
bun install
```

### 2. Environment Variables

Copy `frontend/.env.example` to `frontend/.env`. The public variables exposed via `$env/dynamic/public`:

| Variable             | Purpose                                              | Example                 |
| -------------------- | ---------------------------------------------------- | ----------------------- |
| `PUBLIC_BACKEND_URL` | Base URL of the FastAPI backend (HTTP).              | `http://localhost:8000` |
| `PUBLIC_WS_URL`      | Base URL for the rooms WebSocket (`ws://`/`wss://`). | `ws://localhost:8000`   |

### 3. Running the Dev Server

```bash
bun dev

# or open in browser automatically
bun dev --open
```

The app will be available at `http://localhost:5173/`.

### 4. Building for Production

```bash
bun run build
```

The project uses `@sveltejs/adapter-node`; the build output is a Node server suitable for the bundled `Dockerfile`.

### 5. Previewing the Production Build

```bash
bun run preview
```

## Routes

- `/` — Landing page.
- `/auth` — Mnemonic input, signs the auth challenge locally, and exchanges the resulting JWT for an httpOnly `session` cookie via the SvelteKit form action.
- `/rooms` — Lists active rooms, subscribes to the `/ws/rooms` WebSocket for live updates, and exposes create/join/leave actions for authenticated users.
- `/test` — Internal scratchpad route.

## Authentication (BFF Pattern)

The JWT issued by the backend never reaches client-side JavaScript. The flow:

1. The client derives the identity from the mnemonic and signs the backend nonce locally (`ethers` / `viem`).
2. The signed proof is sent to the backend, which returns a JWT.
3. The JWT is posted to the SvelteKit `login` action in `routes/auth/+page.server.ts`, which stores it in an `httpOnly`, `sameSite=strict` cookie named `session`.
4. Server-side loaders read the cookie, decode the JWT (`jwt-decode`), and expose only the address/username to the page.

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── assets/                # Static assets imported by components
│   │   ├── components/
│   │   │   └── MnemonicInput.svelte
│   │   ├── auth.ts                # Client-side mnemonic derivation & signing helpers
│   │   ├── roomsStore.ts          # Svelte store backed by the rooms WebSocket
│   │   ├── global.css             # Global styles
│   │   └── index.ts               # Public re-exports
│   ├── routes/
│   │   ├── +layout.svelte
│   │   ├── +page.svelte           # Landing page
│   │   ├── auth/                  # Sign-in flow (+page.svelte, +page.server.ts)
│   │   ├── rooms/                 # Rooms browser (+page.svelte, +page.server.ts)
│   │   └── test/
│   └── app.html
├── static/
├── tsconfig.json
├── package.json
├── svelte.config.js
└── vite.config.js
```

## Quality Control

```bash
bun run check    # svelte-check + TypeScript
bun run lint     # ESLint
bun run format   # Prettier
```

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte extension](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).
