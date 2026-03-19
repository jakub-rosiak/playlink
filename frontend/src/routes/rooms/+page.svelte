<script>
    import { roomsStore } from "$lib/roomsStore";
</script>

{#each $roomsStore as room}
    <div>
        {room.name} ({room.players_active}/{room.players_max})
    </div>
{/each}
