import { writable } from "svelte/store";

function createRoomsStore() {
  const { subscribe, set } = writable([]);

  let reconnectTimeout = null;
  let ws = null;

  function connect() {
    ws = new WebSocket("ws://localhost:8000/ws/rooms"); // path tymczasowy, jak cos to sie zmieni

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      set(JSON.parse(event.data));
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected, retrying...");
      reconnect();
    };

    ws.onerror = () => {
      ws.close();
    };
  }

  function reconnect() {
    clearTimeout(reconnectTimeout);
    reconnectTimeout = setTimeout(connect, 1000);
  }

  connect();

  return {
    subscribe,
  };
}

export const roomsStore = createRoomsStore();
