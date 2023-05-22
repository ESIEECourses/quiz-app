<template>
    <header class="header">
      <nav>
        <RouterLink to="/"><h1 class="texto">Home</h1></RouterLink>
        <RouterLink to="/admin"><h1 class="texto">Admin</h1></RouterLink>
      </nav>
    </header>

    <main>  
      <RouterView />
    </main>
</template>



<script>
import { RouterLink, RouterView } from 'vue-router';

export default {
  name: 'App',
  components: {
    RouterLink,
    RouterView,
  },
};
</script>


<style>
.header {
  background-color: #333;
  color: #fff;
  padding: 20px;
  position: relative;
  z-index: 10;
}

.header nav {
  display: flex;
  justify-content: center;
}

.header nav a {
  margin: 0 10px;
  color: #fff;
  text-decoration: none;
}
</style>