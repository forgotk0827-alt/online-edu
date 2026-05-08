<template>
  <div>
    <h1 class="page-title">{{ title }}</h1>
    <div class="heart-divider">♥</div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true }
});
</script>
