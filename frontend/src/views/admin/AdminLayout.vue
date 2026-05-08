<template>
  <main class="admin-body">
    <div class="admin-shell">
      <AdminSidebar />
      <section class="admin-main">
        <router-view />
      </section>
    </div>
  </main>
</template>

<script setup>
import AdminSidebar from "../../components/AdminSidebar.vue";
</script>
