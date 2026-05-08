<template>
  <main class="client-page">
    <ClientNav />
    <section class="container">
      <slot />
    </section>
  </main>
</template>

<script setup>
import ClientNav from "./ClientNav.vue";
</script>
