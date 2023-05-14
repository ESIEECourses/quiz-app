<template>
  <div>
    <header>
      <div class="wrapper">
        <nav>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
        </nav>
      </div>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
header {
  background-color: #333;
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}

.wrapper {
  display: flex;
  justify-content: center;
}

nav {
  font-size: 1rem;
}

nav a {
  display: inline-block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #333;
}

nav a.router-link-active {
  color: #000;
  font-weight: bold;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
  }

  nav {
    margin-left: 2rem;
  }
}
</style>
